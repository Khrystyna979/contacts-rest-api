from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, extract
from src.db.models import Contact
from src.schemas.contacts import ContactModel, ContactUpdate
from datetime import date, timedelta

async def read_contacts(skip: int, 
                        limit: int, 
                        first_name: str | None, 
                        last_name: str | None, 
                        email: str | None, 
                        db: AsyncSession) -> List[Contact]:
    
    stmt = select(Contact)
    filters = []
    if first_name:
        filters.append(Contact.first_name.ilike(f'%{first_name}%'))
    if last_name:
        filters.append(Contact.last_name.ilike(f'%{last_name}%'))
    if email:
        filters.append(Contact.email.ilike(f'%{email}%'))
        
    if filters:
        stmt = stmt.where(and_(*filters))
        
    result = await db.scalars(stmt.offset(skip).limit(limit))
    return result.all()

async def read_contact(contact_id: int, db: AsyncSession) -> Contact | None:
    stmt = select(Contact).where(Contact.id == contact_id)
    contact = await db.scalar(stmt)
    return contact

async def create_contact(body: ContactModel, db: AsyncSession) -> Contact:
    new_contact = Contact(**body.model_dump())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

async def update_contact(contact_id: int, body: ContactUpdate, db: AsyncSession) -> Contact | None:
    stmt = select(Contact).where(Contact.id == contact_id)
    contact = await db.scalar(stmt)
    if contact:
        update_data = body.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(contact, key, value)
            
        await db.commit()
        await db.refresh(contact)
        return contact
    return None

async def delete_contact(contact_id: int, db: AsyncSession) -> Contact | None:
    stmt = select(Contact).where(Contact.id == contact_id)
    contact = await db.scalar(stmt)
    if contact:
        await db.delete(contact)
        await db.commit()
        return contact
    return None

async def read_contacts_birthdays(days: int, db: AsyncSession) -> List[Contact]:
    today_date = date.today()
    end_date = today_date + timedelta(days=days)

    today_doy = today_date.timetuple().tm_yday
    end_doy = end_date.timetuple().tm_yday

    if today_doy <= end_doy:
        stmt = select(Contact).where(
            extract('doy', Contact.birthday).between(today_doy, end_doy)
        )
    else:
        stmt = select(Contact).where(
            or_(
                extract('doy', Contact.birthday) >= today_doy,
                extract('doy', Contact.birthday) <= end_doy
            )
        )

    contacts = await db.scalars(stmt)
    return contacts.all()


