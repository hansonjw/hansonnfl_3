users = {1:"Grandpa", 2:"Michele", 3:"Ryan", 4:"Kerry", 5:"Keira", 6:"Tegan", 7:"Justin", 8:"Regina"}
games = [1, 2, 3, 4, 5, 6, 7]
pick = 1

# pick: id, user, game, team

for key in users.keys():
    print(f"--{users[key]}'s picks")
    for game in games:
        print(
            f"INSERT INTO pick VALUES({pick}, {key}, {game}, );"
        )
        pick += 1


nfl = Team(id=0, teamname='nfl', league_id=0)
niners = Team(id=1, teamname='49ers', league_id=2)
bengals = Team(id=2, teamname='bengals', league_id=1)
bills = Team(id=3, teamname='bills', league_id=1)
bucs = Team(id=4, teamname='bucs', league_id=2)
chiefs = Team(id=5, teamname='chiefs', league_id=1)
packers = Team(id=6, teamname='packers', league_id=2)
rams = Team(id=7, teamname='rams', league_id=2)
titans = Team(id=8, teamname='titans', league_id=1)


nfl_league = League(id=0, name='NFL')
afc = League(id=1, name='AFC')
nfc = League(id=2, name='NFC')