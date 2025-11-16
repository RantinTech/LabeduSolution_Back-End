def map_user_record(record: dict):
    return {
        "id": record.get("id"),
        "name": record.get("Name"),
        "surname": record.get("Surname"),
        "cpf": record.get("Cpf"),
        "photo_profile": record.get("Photo_Profile"),
        "date_register": record.get("Date_Register"),
        "date_acess": record.get("Date_Acess"),
        "admin": record.get("Admin"),
    }
