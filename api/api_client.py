import requests
from sqlalchemy import create_engine, Column, Integer, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Text, nullable=False)
    is_submitted = Column(Boolean, default=False)


class APIClient:

    def __init__(self, api_url, db_path="sqlite:///local_attendance.db"):
        self.api_url = api_url
        self.engine = create_engine(db_path, echo=False, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # -------------------------------
    # LOCAL STORAGE
    # -------------------------------
    def save_locally(self, data):
        """Store data locally with is_submitted=False"""
        submission = Submission(data=str(data), is_submitted=False)
        self.session.add(submission)
        self.session.commit()
        print("💾 Data saved locally.")

    # -------------------------------
    # API SUBMISSION
    # -------------------------------
    def submit(self, data):
        try:
            response = requests.post(self.api_url, json=data, timeout=5)
            response.raise_for_status()
            print("✅ Data submitted successfully.")
            return True
        except requests.RequestException:
            print("⚠️ No internet / submission failed / Internal Error 505. Saving locally...")
            self.save_locally(data)
            return False

    def submit_pending(self):
        pending_rows = self.session.query(Submission).filter_by(is_submitted=False).all()
        for row in pending_rows:
            try:
                data_dict = eval(row.data) if isinstance(row.data, str) else row.data
                if self.submit(data_dict):
                    row.is_submitted = True
                    self.session.commit()
            except Exception as e:
                print("❌ Failed to submit row:", e)

    def close(self):
        self.session.close()
        self.engine.dispose()
