import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


engine = sqlalchemy.create_engine('sqlite:///./instance/nfl.db', pool_pre_ping=True)
# Session = sessionmaker(bind=engine)

# these two lines perform the "database reflection" to analyze tables and relationships
Base = automap_base()
Base.prepare(engine, reflect=True)

# there are many tables in the database but I want `products` and `categories`
# only so I can leave others out
Team = Base.classes.team
Game = Base.classes.game
League = Base.classes.league

session = Session(bind=engine)

teams = session.query(Team).all()
games = session.query(Game).all()
leagues = session.query(League).all()

def generate_code(qryList):
    codeOutput=""
    codeList = []
    for qryObj in qryList:
        if qryList == teams:
            if qryObj.teamname[0].isdigit():
                codeLineId = f"_{qryObj.teamname}"
            else:
                codeLineId = qryObj.teamname
            codeStr = f"{codeLineId}=Team("
        elif qryList == games:
            codeLineId = f"game_{qryObj.id}"
            codeStr = f"{codeLineId}=Game("
        elif qryList == leagues:
            codeLineId = f"league_{qryObj.id}"
            codeStr = f"{codeLineId}=League("
        
        for key in qryObj.__table__.columns.keys():
            objItem = getattr(qryObj, key)
            if type(objItem) is int:
                codeStr = codeStr + f"{key}={getattr(qryObj, key)}"
            else:
                codeStr = codeStr + f"{key}='{getattr(qryObj, key)}'"

            if key == qryObj.__table__.columns.keys()[-1]:
                codeStr = codeStr + ")\n"
            else:
                codeStr = codeStr + ", "
        codeOutput = codeOutput + codeStr
        
        codeList.append(codeLineId)
    
    return codeOutput, codeList

with open('./nfl/db_seed/loadTables.py', 'w') as f:
    for obj in [teams, games, leagues]:
        code_to_write = generate_code(obj)
        f.write(code_to_write[0])
        for item in code_to_write[1]:
            f.write(
                f"db.session.add({item})\n"
            )
    f.write("db.session.commit()")
with open('./nfl/db_seed/loadTables.py', 'r') as f:
    print(f.read())
