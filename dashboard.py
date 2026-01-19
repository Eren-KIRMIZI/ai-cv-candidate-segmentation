import sqlite3

def get_dashboard_data():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Total aday
    c.execute("SELECT COUNT(*) FROM cvs")
    total = c.fetchone()[0]

    # Uygun aday
    c.execute("SELECT COUNT(*) FROM cvs WHERE status = 'Uygun'")
    uygun = c.fetchone()[0]

    # Uygun olmayan
    uygun_degil = total - uygun

    # Pozisyona göre aday sayısı
    c.execute("""
        SELECT position, COUNT(*) 
        FROM cvs 
        GROUP BY position
    """)
    position_counts = c.fetchall()

    # Ortalama skor
    c.execute("""
        SELECT position, ROUND(AVG(score) * 100, 2)
        FROM cvs
        GROUP BY position
    """)
    avg_scores = c.fetchall()

    # Seniority dağılımı
    c.execute("""
        SELECT seniority, COUNT(*)
        FROM cvs
        GROUP BY seniority
    """)
    seniority_counts = c.fetchall()

    conn.close()

    return {
        "total": total,
        "uygun": uygun,
        "uygun_degil": uygun_degil,
        "position_counts": position_counts,
        "avg_scores": avg_scores,
        "seniority_counts": seniority_counts
    }