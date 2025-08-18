from datetime import timedelta
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import security
from database import engine, get_db, Base
from models.user import User as UserModel
import models
from schemas import (
    user as UserSchema,
    team as TeamSchema,
    tournament as TournamentSchema,
    token as TokenSchema,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/token", response_model=TokenSchema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=UserSchema.User)
def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/me/", response_model=UserSchema.User)
def read_users_me(current_user: UserModel = Depends(security.get_current_user)):
    return current_user


@app.post("/teams/", response_model=TeamSchema.Team)
def create_team(
    team: TeamSchema.TeamCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(security.get_current_user),
):
    return crud.create_team(db=db, team=team)


@app.get("/teams/", response_model=List[TeamSchema.Team])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, skip=skip, limit=limit)


@app.post("/teams/{team_id}/join", response_model=UserSchema.User)
def join_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(security.get_current_user),
):
    team = crud.get_team(db, team_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    if current_user.team_id is not None:
        raise HTTPException(status_code=400, detail="User is already in a team")
    return crud.assign_user_to_team(db, user=current_user, team_id=team_id)


@app.post("/tournaments/", response_model=TournamentSchema.Tournament)
def create_tournament(
    tournament: TournamentSchema.TournamentCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(security.get_current_user),
):
    return crud.create_tournament(db=db, tournament=tournament)


@app.get("/tournaments/", response_model=List[TournamentSchema.Tournament])
def read_tournaments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tournaments(db, skip=skip, limit=limit)
