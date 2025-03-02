from app.models import GeneratedText
from app.extensions import db

class TextService:
    @staticmethod
    def save_generated_text(user_id, prompt, response):
        new_text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        db.session.add(new_text)
        db.session.commit()
        return new_text

    @staticmethod
    def get_text_by_id(text_id, user_id) -> GeneratedText:
        return GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()

    @staticmethod
    def update_text(text: GeneratedText, new_response) -> GeneratedText:
        text.response = new_response
        text.updated_at = db.func.now()
        db.session.commit()
        return text

    @staticmethod
    def delete_text(text_id, user_id):
        text = TextService.get_text_by_id(text_id, user_id)
        if text:
            db.session.delete(text)
            db.session.commit()
            return True
        return False
