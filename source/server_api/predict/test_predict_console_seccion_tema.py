from predictSeccionTema import PredictSeccionTema
from template_classes import normalize_text

def main():
    clasifier = PredictSeccionTema(root_path = "../../../",
                    feature_file = "calcFeat_tfid_hash28_n10000_svd1000.p",
                    features_path = 'data/features/',
                    path_model_seccion = 'models/test/',
                    path_model_tema = 'models/seccion/')

    test_text = 'Un total de 916 personas murieron en acciones que involucraron a la policía y otras 2.989 fallecieron en homicidios dolosos, durante los ochos meses de intervención de la seguridad pública en Río de Janeiro, la ciudad más emblemática de Brasil, según informe divulgado este lunes por una ONG.Las muertes de miembros de la Policía y el Ejército durante el período en que ha sido implementada la intervención, también fueron retomadas en el informe, según el cual 74 agentes han fallecido entre febrero y octubre de 2018."Las políticas de guerra contra las drogas y los enfrentamientos como método de seguridad pública son responsables por los inaceptables números de Río de janeiro: además de las muertes de civiles y militares, casi mil muertes de civiles por acción policial", aseguró el informe de la ONG.Los datos se recogen en un informe divulgado este martes por el Observatorio de la Intervención del Centro de Estudios de Seguridad y Ciudadanía de la Universidad brasileña Cándido Mendes, a través de las redes sociales.'
    clasifier.predict(test_text)
    test_text = 'El Banco Falabella se convertirá en el mayor emisor de tarjetas de crédito del país, después de que la Superintendencia de Bancos e Instituciones Financieras (SBIF) aprobara la integración de CMR Falabella a la compañía. La figura bajo la cual CMR se integra a Banco Falabella es la de Sociedad de Apoyo al Giro (SAG). Con esto, Banco Falabella será el mayor emisor de tarjetas de crédito del país, con una cantidad superior a los 3 millones de ellas activas, según Diario Financiero.'
    clasifier.predict(test_text)    

if __name__ == '__main__':
    main()