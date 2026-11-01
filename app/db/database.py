from sqlalchemy import create_engine, Column, Integer, String, JSON, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///./frp_engine.db"

# FastAPI ile uyumlu, thread-safe SQLite motoru
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    system = Column(String) # D&D 5e, Fate Core, CoC
    session_zero_data = Column(JSON) # Pydantic modelinden dönen JSON (Lines, Veils, Tone)
    
    characters = relationship("Character", back_populates="campaign", cascade="all, delete-orphan")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    name = Column(String, index=True)
    stats = Column(JSON) # Karakter kağıdı metrikleri
    motivations = Column(Text)
    
    campaign = relationship("Campaign", back_populates="characters")

def init_db():
    """Veritabanı tablolarını oluşturur."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI Dependency Injection için veritabanı oturumu sağlar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Operasyonları
def create_campaign(db, name: str, system: str, session_zero_data: dict):
    new_campaign = Campaign(name=name, system=system, session_zero_data=session_zero_data)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

def create_character(db, campaign_id: int, name: str, stats: dict, motivations: str):
    new_char = Character(campaign_id=campaign_id, name=name, stats=stats, motivations=motivations)
    db.add(new_char)
    db.commit()
    db.refresh(new_char)
    return new_char