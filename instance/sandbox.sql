SELECT g_id, game_desc, team_source, sort_order, teamname AS team_qry, "<div class='col'><img src='.././static/"||teamname||".png' class='team-pickem'/></div>" AS tag FROM

(SELECT g.id AS g_id, g.teamhome AS team_qry, 'Home Team' AS team_source, -3 AS sort_order FROM game g
UNION
SELECT g.id AS g_id, g.teamvisitor AS team_qry, 'Away Team' AS team_source, -2 AS sort_order FROM game g
UNION
SELECT g.id AS g_id, g.winner AS team_qry, 'Winner' AS team_source, -1 AS sort_order FROM game g
UNION
SELECT p.game_id AS g_id, team_id AS team_qry, u.displayname AS team_source, u.id AS sort_order FROM pick p LEFT JOIN user u
ON p.user_id = u.id

ORDER BY g.id ASC, sort_order ASC)

LEFT JOIN team t ON team_qry = t.id
LEFT JOIN game on g_id = game.id;



SELECT id, game_desc from game;

SELECT id, displayname from user;


SELECT p.game_id, t.teamname FROM pick p
LEFT JOIN team t ON
p.team_id = t.id
WHERE p.user_id=7
ORDER BY p.game_id ASC;