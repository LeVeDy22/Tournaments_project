from sqlalchemy.orm import Session

from models import user as UserModel, team as TeamModel, tournament as TournamentModel
from schemas import user as UserSchema, relations as RelationsSchema
import security


def get_user(db: Session, user_id: int):
    return db.query(UserModel.User).filter(UserModel.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel.User).filter(UserModel.User.email == email).first()


def create_user(db: Session, user: UserSchema.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = UserModel.User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def assign_user_to_team(db: Session, user: UserModel.User, team_id: int):
    user.team_id = team_id
    db.commit()
    db.refresh(user)
    return user


def get_team(db: Session, team_id: int):
    return db.query(TeamModel.Team).filter(TeamModel.Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TeamModel.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: RelationsSchema.TeamCreate):
    db_team = TeamModel.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_tournaments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TournamentModel.Tournament).offset(skip).limit(limit).all()


def get_tournament(db: Session, tournament_id: int):
    return (
        db.query(TournamentModel.Tournament)
        .filter(TournamentModel.Tournament.id == tournament_id)
        .first()
    )


def create_tournament(db: Session, tournament: RelationsSchema.TournamentCreate):
    db_tournament = TournamentModel.Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def register_team_for_tournament(
    db: Session, team: TeamModel.Team, tournament: TournamentModel.Tournament
):
    tournament.teams.append(team)
    db.commit()
    return tournament
