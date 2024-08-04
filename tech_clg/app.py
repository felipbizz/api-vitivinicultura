import datetime
from enum import Enum
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, validator
from unidecode import unidecode

from tech_clg.vitivinicultura import Vitivinicultura

app = FastAPI()
vt = Vitivinicultura()

modified_date = vt.get_last_updated_date()
ultima_data_coletada = datetime.date(2023, 12, 21)

vt.get_df_dict(modified_date, ultima_data_coletada)
df_dict = vt.df_dict


class DFKeys(str, Enum):
    Producao = 'Producao'
    ProcessaViniferas = 'ProcessaViniferas'
    ProcessaAmericanas = 'ProcessaAmericanas'
    ProcessaMesa = 'ProcessaMesa'
    Comercio = 'Comercio'
    ImpVinhos = 'ImpVinhos'
    ImpEspumantes = 'ImpEspumantes'
    ImpFrescas = 'ImpFrescas'
    ImpPassas = 'ImpPassas'
    ImpSuco = 'ImpSuco'
    ExpVinho = 'ExpVinho'
    ExpEspumantes = 'ExpEspumantes'
    ExpUva = 'ExpUva'
    ExpSuco = 'ExpSuco'


max_year = ultima_data_coletada.year
min_year = 1970


class GetDataRequest(BaseModel):
    df_key: DFKeys
    year: Optional[int] = Field(None, ge=min_year, le=max_year)

    @validator('year')
    def validate_year(cls, v):
        if v is not None:
            if v < min_year or v > max_year:
                raise ValueError(f'Year must be between {min_year} and {max_year}')
        return v


fake_users_db = {
    'felipe': {
        'username': 'felipe',
        'full_name': 'Felipe Bizzo',
        'email': 'johndoe@example.com',
        'hashed_password': 'secret',
        'disabled': False,
    }
}


def fake_hash_password(password: str):
    return password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # autenticação fake, somente para exemplo
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


@app.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail=f'Incorrect username {user_dict}')
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail=f'Incorrect password {user.hashed_password} and {hashed_password}',
        )

    return {'access_token': user.username, 'token_type': 'bearer'}


@app.post('/retorna_dados/')
async def get_data(data: GetDataRequest, Authorization: str = Depends(oauth2_scheme)):
    """
    Function to retrieve data based on the key and optional year
    """
    df_key = data.df_key
    year = data.year

    table_type = {
        'produto': ['Producao', 'ProcessaAmericanas'],
        'cultivar': ['ProcessaViniferas', 'ExpUva', 'ExpSuco'],
    }

    if df_key not in df_dict:
        raise HTTPException(
            status_code=404,
            detail={
                'error': f"Dataframe '{df_key}' not found.\
                           Select one of this options {list(df_dict)}"
            },
        )
    try:
        df = vt.get_tabela_especifica(df_key)
        df.columns = df.columns.str.lower()
        df.columns = [unidecode(col) for col in df.columns]
        if year:
            year = str(year)
            if year not in df.columns:
                raise HTTPException(
                    status_code=404,
                    detail={'error': f"Year '{year}' not found in '{df_key}'"},
                )
            if df_key in table_type['produto']:
                filter_columns = ['produto', f'{year}']
            elif df_key in table_type['cultivar']:
                filter_columns = ['cultivar', f'{year}']
            else:
                filter_columns = ['pais', f'{year}']
            if not set(filter_columns).issubset(df.columns):
                raise HTTPException(
                    status_code=404,
                    detail={
                        'error': f"Expected columns {filter_columns} not found in '{df_key}'"
                    },
                )
            data = df[filter_columns].to_dict(orient='records')
        else:
            data = df.to_dict(orient='records')
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail={'error': f'Unexpected error: {e}'})


# # -------------
# STATIC_TOKEN = "token_estatico"

# def verify_token(auth_header: str):
#     """Verifies the provided authentication token."""
#     print('A autorização é:', auth_header, 'e deve ser igual à ', f"Bearer {STATIC_TOKEN}")
#     if not auth_header or auth_header != f"Bearer {STATIC_TOKEN}":
#         raise HTTPException(status_code=401, detail="Unauthorized")
