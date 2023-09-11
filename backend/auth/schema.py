from pydantic import BaseModel


class SendOTP(BaseModel):
    phone_number: str

    class Config:
        from_attributes = True


class VerifyOTP(BaseModel):
    phone_number: str
    otp: int

    class Config:
        from_attributes = True
