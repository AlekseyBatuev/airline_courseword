import sqlite3
from itertools import chain


class Funcs:
    def __init__(self):
        self.airline_bd = sqlite3.connect('Airline.db')
        self.airports_bd = sqlite3.connect("Airports.db")
        self.parking_bd = sqlite3.connect("Parking.db")
        self.airline_cur = self.airline_bd.cursor()
        self.airports_cur = self.airports_bd.cursor()
        self.parking_cur = self.parking_bd.cursor()

    # 1. Посчитать рентабельность рейсов
    def flights_profitability(self):
        flight_id, jet_id, airports, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost = list(
            zip(*self.airline_cur.execute(f'''
            SELECT flight_id, jet_id, arrival_point, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost 
            FROM Flights
        ''').fetchall()))

        models = [self.airline_bd.execute(f'''
            SELECT model_name 
            FROM "Jets" 
            WHERE jet_id == "{i}"
        ''').fetchone()[0] for i in jet_id]

        classes = [self.airline_bd.execute(f'''
            SELECT class_name 
            FROM "Models" 
            WHERE model_name == "{i}"
        ''').fetchone()[0] for i in models]

        maintenance_cost = [self.airports_cur.execute(f'''
            SELECT maintenance_cost 
            FROM "{airports[i]}" 
            WHERE class == "{classes[i]}"
        ''').fetchone()[0] for i in range(len(airports))]

        income = list(map(lambda x, y: x * y, ticket_price, number_of_tickets_sold))
        expenses = list(map(sum, zip(depreciation_cost, fuel_cost, maintenance_cost)))

        return [["№Рейса", "Рентабельность"], flight_id, [round(x/y, 2) for x, y in zip([i-j for i, j in zip(income, expenses)], expenses)]]


    # 2. Посчитать налет самолетов (за месяц, например)
    def flight_time(self):
        jet_id = list(chain(*self.airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
        travel_times_list = [self.airline_bd.execute(f'''
            SELECT travel_time 
            FROM Flights 
            WHERE jet_id == "{i}"
        ''').fetchall() for i in jet_id]

        return [["№Самолета", "Налет"], jet_id, [sum(list(chain(*lists_of_lists))) for lists_of_lists in travel_times_list]]



    # 3. Посчитать “заполняемость” рейса в % за месяц.
    def flight_occupancy(self):
        flight_id, jet_id, number_of_tickets_sold = list(zip(*self.airline_cur.execute(f'''
            SELECT flight_id, jet_id, number_of_tickets_sold 
            FROM Flights
        ''').fetchall()))

        models = [self.airline_bd.execute(f'''
            SELECT model_name 
            FROM "Jets" 
            WHERE jet_id == "{i}"
        ''').fetchone()[0] for i in jet_id]

        number_of_passangers = [self.airline_bd.execute(f'''
            SELECT number_of_passengers 
            FROM "Models" 
            WHERE model_name == "{i}"
        ''').fetchone()[0] for i in models]

        ratio = list(map(lambda x, y: round(x / y, 2), number_of_tickets_sold, number_of_passangers))

        return [["№Рейса", "Заполняемость"], flight_id, ratio]

    # 4. Посчитать стоимость простоя самолетов.
    def parking_cost(self):
        jet_id = list(chain(*self.airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
        models = [self.airline_bd.execute(f'''
            SELECT model_name 
            FROM "Jets" 
            WHERE jet_id == "{i}"
        ''').fetchone()[0] for i in jet_id]

        classes = [self.airline_bd.execute(f'''
            SELECT class_name 
            FROM "Models" 
            WHERE model_name == "{i}"
        ''').fetchone()[0] for i in models]

        airports = list(chain(*self.parking_cur.execute(f'''
            SELECT name 
            FROM sqlite_master 
            WHERE type='table';
        ''').fetchall()))

        airports.remove('sqlite_sequence')

        parking_hours = [[self.parking_cur.execute(f'''
            SELECT "hours" 
            FROM "{i}" 
            WHERE jet_id == "{j}"
        ''').fetchall()[0][0] for i in airports] for j in jet_id]

        airports_hours_dict = list(dict(zip(airports, i)) for i in parking_hours)

        cost_lists = [[self.airports_bd.execute(f'''
            SELECT parking_cost 
            FROM "{key}" 
            WHERE class == "{classes[i]}"
        ''').fetchone()[0] * val for key, val in airports_hours_dict[i].items()] for i in range(len(classes))]

        return [["№Самолета", "Стоимость простоя"], jet_id, list(map(sum, cost_lists))]

