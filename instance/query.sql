SELECT p.id, u.displayname, g.game_desc, p.team_id, t.teamname FROM pick p
    LEFT JOIN user u ON p.user_id = u.id
    LEFT JOIN game g ON p.game_id = g.id
    LEFT JOIN team t ON p.team_id = t.id 


SELECT g.game_desc FROM pick p
    LEFT 