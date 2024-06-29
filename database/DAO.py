from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():
    @staticmethod
    def getNodes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query= """select Distinct(Chromosome)
                from genes g 
                where g.Chromosome != 0"""
        cursor.execute(query, )
        for row in cursor:
            result.append(row['Chromosome'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct  i.GeneID1, i.GeneID2, g1.Chromosome as C1, g2.Chromosome as C2, Expression_Corr
                    from interactions i, genes g1, genes g2
                    where g1.GeneID = i.GeneID1 and g2.GeneID = i.GeneID2 and g1.Chromosome != g2.Chromosome and g1.Chromosome != 0 and g2.Chromosome != 0"""
        cursor.execute(query, )
        for row in cursor:
            result.append((row['GeneID1'],
                          row['GeneID2'],
                          row['C1'],
                          row['C2'],
                          row['Expression_Corr']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getGenes():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from genes g 
                    where g.Chromosome != 0"""
        cursor.execute(query, )
        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result
