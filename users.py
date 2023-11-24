from firebase_admin import auth

def register_user(email, password):
    user = auth.create_user(
        email=email,
        password=password
    )
    return user.uid  # Retorna el ID único del usuario recién creado

def verify_user(token):
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token.get('uid')
    return uid  # Retorna el ID único del usuario verificado
