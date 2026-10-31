from datetime import datetime, timedelta
import database

def calcular_ritmo(total_metros, total_minutos):
    if total_metros > 0:
        min_por_100m = (total_minutos / total_metros) * 100
        minutos_ritmo = int(min_por_100m)
        segundos_ritmo = int((min_por_100m - minutos_ritmo) * 60)
        return f"{minutos_ritmo}:{segundos_ritmo:02d} /100m"
    return "0:00 /100m"

def dias_decorridos_semana(hoje):
    return hoje.weekday() + 1

def obter_estatisticas_periodos():
    todos_treinos = database.buscar_todos_treinos_db()
    hoje = datetime.now()
    
    inicio_semana = (hoje - timedelta(days=hoje.weekday())).strftime("%Y-%m-%d")
    fim_semana = (hoje + timedelta(days=6 - hoje.weekday())).strftime("%Y-%m-%d")
    inicio_mes = hoje.strftime("%Y-%m-01")
    inicio_ano = hoje.strftime("%Y-01-01")

    treinos_semana = [t for t in todos_treinos if inicio_semana <= t[1] <= fim_semana]
    treinos_mes = [t for t in todos_treinos if inicio_mes <= t[1]]
    treinos_ano = [t for t in todos_treinos if inicio_ano <= t[1]]

    def processar(lista_treinos, total_dias):
        metros = sum(t[2] for t in lista_treinos)
        minutos = sum(t[3] for t in lista_treinos)
        calorias = sum(t[4] for t in lista_treinos)
        horas = minutos / 60.0
        ritmo = calcular_ritmo(metros, minutos)
        media_diaria = metros / total_dias if total_dias > 0 else 0
        return {
            "metros": metros,
            "horas": horas,
            "calorias": calorias,
            "ritmo": ritmo,
            "media_diaria": media_diaria
        }

    return {
        "semana": processar(treinos_semana, dias_decorridos_semana(hoje)),
        "mes": processar(treinos_mes, hoje.day),
        "ano": processar(treinos_ano, (hoje - datetime(hoje.year, 1, 1)).days + 1)
    }
