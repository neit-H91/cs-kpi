import psycopg2

conn = psycopg2.connect(
    database ='csdm',
    user ='cskpi',
    password='cskpi',
    host='localhost',
    port='5432',
)

def get_bomb_perf():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    total_planted::numeric / NULLIF(total_rounds, 0) AS bombes_plantées,
    total_won::numeric / NULLIF(total_planted, 0) AS winrate_postplant,
    total_defused::numeric / NULLIF(total_planted, 0) AS bombes_desamorcées
    FROM (
        SELECT
            (SELECT COUNT(*) FROM rounds) AS total_rounds,
            (SELECT COUNT(*) FROM bombs_planted) AS total_planted,
            (
                SELECT COUNT(*)
                FROM bombs_planted b
                JOIN rounds r ON b.match_checksum = r.match_checksum AND b.round_number = r.number
                WHERE r.winner_side = 2 AND b.tick < r.end_tick
            ) AS total_won,
            (SELECT COUNT(*) FROM bombs_defused) AS total_defused
    ) AS subquery;
    """)

    data = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    return list(zip(columns, data))

def get_eco_distrib():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
    ROUND(
        (SUM(CASE WHEN team_a_economy_type = 'pistol' THEN 1 ELSE 0 END) +
         SUM(CASE WHEN team_b_economy_type = 'pistol' THEN 1 ELSE 0 END))
        * 1.0 / (COUNT(*) * 2), 2
    ) AS pistol,
    ROUND(
        (SUM(CASE WHEN team_a_economy_type = 'eco' THEN 1 ELSE 0 END) +
         SUM(CASE WHEN team_b_economy_type = 'eco' THEN 1 ELSE 0 END))
        * 1.0 / (COUNT(*) * 2), 2
    ) AS eco
    ,
    ROUND(
        (SUM(CASE WHEN team_a_economy_type = 'force-buy' THEN 1 ELSE 0 END) +
         SUM(CASE WHEN team_b_economy_type = 'force-buy' THEN 1 ELSE 0 END))
        * 1.0 / (COUNT(*) * 2), 2
    ) AS force,
    ROUND(
        (SUM(CASE WHEN team_a_economy_type = 'semi' THEN 1 ELSE 0 END) +
         SUM(CASE WHEN team_b_economy_type = 'semi' THEN 1 ELSE 0 END))
        * 1.0 / (COUNT(*) * 2), 2
    ) AS semi,
    ROUND(
        (SUM(CASE WHEN team_a_economy_type = 'full' THEN 1 ELSE 0 END) +
         SUM(CASE WHEN team_b_economy_type = 'full' THEN 1 ELSE 0 END))
        * 1.0 / (COUNT(*) * 2), 2
    ) AS Full
    FROM rounds
    """)

    data = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    return list(zip(columns, data))


def get_eco_kills():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    team_economy_type,
    ROUND(AVG(kill_count), 2) AS avg_kills
FROM (
    SELECT
        r.team_a_economy_type AS team_economy_type,
        COUNT(k.killer_steam_id) AS kill_count
    FROM rounds r
    LEFT JOIN kills k
        ON r.match_checksum = k.match_checksum
        AND r.number = k.round_number
        AND k.killer_team_name = r.team_a_name
    WHERE r.team_a_economy_type IN ('eco', 'force-buy', 'semi', 'full')
    GROUP BY r.match_checksum, r.number, r.team_a_economy_type

    UNION ALL

    SELECT
        r.team_b_economy_type AS team_economy_type,
        COUNT(k.killer_steam_id) AS kill_count
    FROM rounds r
    LEFT JOIN kills k
        ON r.match_checksum = k.match_checksum
        AND r.number = k.round_number
        AND k.killer_team_name = r.team_b_name
    WHERE r.team_b_economy_type IN ('eco', 'force-buy', 'semi', 'full')
    GROUP BY r.match_checksum, r.number, r.team_b_economy_type
) sub
GROUP BY team_economy_type;


    """)
    return cursor.fetchall()

def get_inferno_ct_deaths():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT victim_x, victim_y FROM public.kills k
    join matches m
    on k.match_checksum = m.checksum
    where map_name = 'de_inferno'
    and victim_side = 3
    """)
    
    return cursor.fetchall()

def get_grenade_kpis():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    (SELECT AVG(total)
     FROM (
         SELECT COUNT(*) AS total, match_checksum
         FROM kills
         WHERE is_assisted_flash = true
         GROUP BY match_checksum
     ) AS flash_assist_kills) AS avg_flash_assist,

    (SELECT AVG(health_damage)
     FROM damages
     WHERE weapon_name = 'HE Grenade') AS avg_he_damage,

    (SELECT AVG(sum_dmg)
     FROM (
         SELECT SUM(health_damage) AS sum_dmg, weapon_unique_id
         FROM damages
         WHERE weapon_name IN ('Molotov', 'Incendiary Grenade')
         GROUP BY weapon_unique_id
     ) AS molo_damages) AS avg_molotov_damage
    """)

    data = cursor.fetchone()
    columns = [desc[0] for desc in cursor.description]
    return list(zip(columns, data))


def get_indiv_kpi():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
    steam_id,
    COUNT(*) AS nb_matchs,
    ROUND(AVG(kill_death_ratio)::numeric, 2) AS avg_kd,
    ROUND(AVG(headshot_percentage)::numeric, 2) AS avg_hs
    FROM 
        players
    GROUP BY 
        steam_id;
    """)

    return cursor.fetchall()

def get_elim_distrib():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT total
    FROM (
        SELECT count(*) AS total, match_checksum, killer_name
        FROM kills
        WHERE killer_team_name <> victim_team_name
        AND killer_name <> 'World'
        GROUP BY match_checksum, killer_name
    ) AS subquery
    ORDER BY total ASC;
    """)

    return cursor.fetchall()

def get_clutch_ratios():
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
	opponent_count,
	COUNT(*) AS total_clutches,
	COUNT(CASE WHEN won = true THEN 1 END) AS total_won,
	ROUND(COUNT(CASE WHEN won = true THEN 1 END) * 1.0 / NULLIF(COUNT(*), 0), 5) AS win_ratio
    FROM clutches
    GROUP BY opponent_count
    ORDER BY opponent_count;
                   """)

    return cursor.fetchall()

conn.close