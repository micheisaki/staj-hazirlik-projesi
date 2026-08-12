
from datetime import datetime, timedelta
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="giris")

def sifre_hashle(sifre):
    return pwd_context.hash(sifre)

def sifre_dogrula(girilen_sifre, hashli_sifre):
    return pwd_context.verify(girilen_sifre, hashli_sifre)

    
def token_olustur(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #Token'in 30 dakika sonra geçersiz olacaği zamani hesaplar
    to_encode = data.copy() #Sana verilen data sözlüğünün bir kopyasini alir (orijinali bozmamak için)
    to_encode.update({"exp": expire}) #Bu kopyaya "exp" (expiration/geçerlilik süresi) bilgisini ekler
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #Hepsini SECRET_KEY ile şifreleyip (jwt.encode) bir token string'i olarak döndürür

def gecerli_kullanici(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #Token'i çözmek için jwt.decode kullanılır
        kullanici_adi: str = payload.get("sub") #Token'den "sub" (subject) alanını alır
        if kullanici_adi is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return kullanici_adi
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    


