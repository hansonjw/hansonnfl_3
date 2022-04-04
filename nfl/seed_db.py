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
    