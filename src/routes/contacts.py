from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.db.db import get_db
from src.schemas.contacts import ContactModel, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.get('/', response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, 
                        limit: int = 10, 
                        first_name: str | None = Query(default=None), 
                        last_name: str | None = Query(default=None), 
                        email: str | None = Query(default=None), 
                        db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.read_contacts(skip, limit, first_name, last_name, email, db)
    return contacts
    
@router.get('/birthdays', response_model=List[ContactResponse])
async def read_contacts_birthdays(days: int = 7, db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.read_contacts_birthdays(days, db)
    return contacts
    
    
@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.create_contact(body, db)
    return contact
    
@router.get('/{contact_id}', response_model=ContactResponse) 
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repository_contacts.read_contact(contact_id, db)
    if contact:
        return contact
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    
    
@router.put('/{contact_id}', response_model=ContactResponse)
async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession = Depends(get_db)):
    update_contact = await repository_contacts.update_contact(contact_id, body, db)
    if update_contact:
        return update_contact
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    
@router.delete('/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    deleted_contact = await repository_contacts.delete_contact(contact_id, db)
    if deleted_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Contact not found')
    return None