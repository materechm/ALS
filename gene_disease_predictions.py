from scipy import stats
import itertools
import pprint
import networkx as nx
import csv
import numpy

class DiseaseGeneManager:
  def __init__(self, fileName):
    self.fileName = fileName
    self.disease2genes = {}
    #Maps from diseaseName::String to{geneProbability::string}
    self.graph = nx.Graph()
    #creates a networkx graph
    self.diseases = []
    self.write_file = open('disease_predictions.csv', 'a')
    self.writer = csv.writer(self.write_file, delimiter = '\t')
    self.writer.writerow(("disease 1", "disease 2", "correlation"))

  def load_data_from_csv(self):
    read_file = open(self.fileName)
    reader = csv.reader(read_file, delimiter = '\t')
    fieldnames = reader.next()
    self.diseases = fieldnames[1:]
    data = numpy.loadtxt(self.fileName, dtype = float, delimiter = '\t', skiprows = 1, usecols = range(1, 24))
    for disease in self.diseases:
      self.disease2genes[disease] = data[:, self.diseases.index(disease)]
    read_file.close()

  def calculate_correlation(self, disease1, disease2):
    correlation = stats.spearmanr(self.disease2genes[disease1], self.disease2genes[disease2])
    write_file = open('disease_predictions.csv', 'wb')
    writer = csv.writer(write_file, delimiter = '\t')
    writer.writerow(("disease 1", "disease 2", "correlation"))
    self.writer.writerow((disease1, disease2, correlation[0]))
    self.graph.add_edge(disease1, disease2, weight = correlation[0])

def main():
  fileName = '/Users/mtchavez/Downloads/prediction-table.txt'
  path = '/Users/mtchavez/documents/predictions_graph.gml'
  dgm = DiseaseGeneManager(fileName)
  dgm.load_data_from_csv()
  for pair in itertools.combinations(dgm.diseases, repeat=2):
    dgm.calculate_correlation(*pair)
  pprint.pprint(dgm.graph.edges(data = True))
  nx.write_gml(dgm.graph, path)

main()
