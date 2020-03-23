

# 2. Apprentissage statistique

## 2.1. Méthodes statistiques et probabilistes

Dans le domaine des interfaces utilisateurs, les chaînes de Markov sont désormais bien implantées pour la prédiction de texte sur les appareils mobiles, notamment les téléphones et les tablettes. Leur utilisation pour d'autres éléments d'interface est également étudiée, voir utilisée (propositions de Siri sur les applications à ouvrir sur iPhone par exemple). Des perspectives innovantes d'utilisation de ces modèles sont aujourd'hui envisagées, comme par exemple l'identification de l'utilisateur en fonction de l'usage qu'il fait de l'interface [1] ou même de sa gestuelle, comme par exemple lorsqu'un téléphone est sorti d'une poche [2]. Les possibilités pourraient s'étendre à tout système embarqué bénéficiant d'une interface, textuelle ou non. En particulier, les appareils de type montres ou lunettes connectées pourraient tout particulièrement bénéficier de ce type d'intelligence embarquée.

Les systèmes embarqués d'aide à la décision, et d'assistance au pilotage de véhicules divers utilisent également des méthodes issues de l'apprentissage statistique : les modèles probabilistes de séries temporelles. Les systèmes de navigation inertiels utilisent toujours les filtres de Kalman, et des autopilotes utilisant des filtres de Kalman étendus sont également étudiés pour des systèmes non linéaires, par exemple pour des drones [3]. Ils peuvent également améliorer la gestion des batteries [4]. Ces filtres peuvent être généralisés par le concept de modèle de Markov caché, qui est massivement utilisé dans des systèmes embarqués pour la reconnaissance de voix (par exemple pour les enceintes intelligentes) et d'écriture (un domaine prometteur pour les tablettes équipées de stylets).

Plus généralement, les modèles probabilistes bayésiens peuvent être utilisés pour détecter le contexte d’emploi d’une interface ou anticiper les recherches des utilisateurs [5]. La programmation bayésienne peut également tenter de prédire les préférences utilisateurs et résoudre le problème d’un jeu de données initial inextistant (*cold start*) qui limite l’efficacité des méthodes nécessitant une période d’apprentissage [6].

## 2.2. Apprentissage automatique classique

Au delà de ces outils statistiques et probabilistes, la révolution de l'aprentissage automatique (*machine learning*) touche également les systèmes embarqués. Ce type d'algorithmes était jusqu'à il y a quelques années limité aux installations fixes spécialisées et aux services dans le *cloud* car il nécessite de gros volumes de données et de fortes capacités de calculs. Or, pour des systèmes embarqués, les données doivent pouvoir être prises en compte de façon incrémentales, souvent à partir d'une base de départ réduite ; en outre, les capacités de calcul sont limitées alors même que les résutlats sont souvent attendus en temps réel ; enfin, les capacités de mémoire sont fortement contraintes. Les capacités des batteries sont également un facteur limitant. Les méthodes d'apprentissage automatique classiques (k plus proches voisins, SVM, forêts d'arbes décisionnels...) fonctionnent mieux que les réseaux de neurones sur des jeux de données réduits, et sont moins gourmands en temps de calcul et en mémoire (en particulier, ils ne nécessitent pas de processeurs spécialisés tels que des GPU) : ils peuvent donc s'avérer plus adaptés dans certains scénarios d'intelligence embarquée dans des situations de contraintes extrêmes, comme par exemple sur des appareils sans alimentation autonome [7].

La maintenance prédictive, les diagnostics en temps réel et la prévention de panne est un champ d'études prometteur pour les intelligences embarquées, en particulier dans le domaine industriel et logistique. Les méthodes statistiques d'apprentissage automatiques peuvent donner de bons résultats, par exemple pour la détermination de l'état d'une machine-outil en temps réel à l'aide de forêts d'arbres décisionnels [8] pour leur explicabilité et leur facilité de débuggage, ou à l'aide de machines à vecteur de support [9], un type avancé de classifieur linéaire particulièrement adapté pour les problème de grande dimensionalité mais avec un nombre réduit d'observations.

Un autre champ d’application concerne la reconnaissance visuelle, dans l’optique de détecter et classer des informations au plus près des appareils (caméras de surveillance, caméras embarquées...) pour parer aux contraintes du *cloud* (*edge computing*). Dans le contexte d’appareils bon marché aux capacités limitées, l’apprentissage automatique peut fournir de bons résultats en temps réels sans recours à des processeurs spécialisés, par exemple pour la reconnaissance gestuelle par des caméras de sécurité intelligentes permettant de détecter au plus vite des comportements violents ou criminels [10].

## 2.3. Intelligence distribuée en périphérie de réseau 

La démocratisation (d’aucuns dirait la prolifération...) des appareils connectés (aussi appelée « Internet des objets ») voit actuellement une tendance au retour partiel de l’intelligence vers les appareils en périphérie de réseau (*edge computing*). Dans ce contexte, l’intelligence embarquée pourrait connaître des évolutions significatives tendant à distribuer le traitement et le stockage des données sans recours systématique au *cloud*.

Des solutions matérielles et logicielles consacrées plus particulièrement à l’intelligence artificielle en périphérie de réseau sont plus particulièrement à l’étude pour tirer parti de composants bon marchés dédiés à l’internet des objets [11]. Étant donné les économies d’échelles envisageables grace à ce type de matériel, l’intelligence distribuée en périphérie de réseau pourrait s’imposer pour certaines applications.

Enfin, le recours croissant à ce type de solutions logicielles permet d’envisager le développement de modèles d’intelligences artificielles distribuées (*swarm intelligence*). Cette forme d’intelligence embarquée multi-agents s’inspire des stratégies de coopération observées chez certains insectes (fourmis, abeilles...) pour permettre à des robots de coopérer de façon autonome et atteindre des objectifs collectifs de façon plus efficace. [12] [13] 

## Références

[1] U. Mahbub, J. Komulainen, D. Ferreira et R. Chellappa, "Continuous Authentication of Smartphones Based on Application Usage", mai 2019.

[2] M. Jin, Y. He, D. Fang, X. Chen, X. Meng et T. Xing, "iGuard: A real-time anti-theft system for smartphones, 2017.

[3] Z. Tan, Y. Wu et J. Zhang, "Fused attitude estimation algorithm based on explicit complementary filter and Kalman filter for an indoor quadrotor UAV", 2018.

[4] I. Jokic, Z. Zecevic et B. Krstajic, “State-of-charge estimation of lithium-ion batteries using extended Kalman filter and unscented Kalman filter”, 2018.

[5] W.-H. Rho et S.-B. Cho, “Context-aware smartphone application category recommender system with modularized Bayesian networks”, 2014.

[6] X. Dai, F. Li, X. Li et H. Liang, “A Novel Recommender System using Hidden Bayesian Probabilistic Model based Collaborative Filtering”, 2019.

[7] B. Islam, Y. Luo, S. Lee et S. Nirjon, "On-Device Training from Sensor Data on Batteryless Platforms", 2019.

[8] F. Küppers, J. Albers et A. Haselhoff, "Random Forest on an Embedded Device for Real-time Machine State Classification", 2019.

[9] W.-L. Chu, C.-J. Lin et K.-C. Kao, "Fault Diagnosis of a Rotor and Ball-Bearing System Using DWT Integrated with SVM, GRNN, and Visual Dot Patterns", november 2019.

[10] Y. Maret, D. Oberson et M. Gavrilova, “Real-Time Embedded System for Gesture Recognition”, 2018.

[11] E. Oyekanlu et K. Scoles, “Towards Low-Cost, Real-Time, Distributed Signal and Data Processing for Artificial Intelligence Applications at Edges of Large Industrial and Internet Networks”, 2018.

[12] T. Hiejima, S. Kawashima, M. Ke et T. Kawahara, “Effectiveness of Synchronization and Cooperative Behavior of Multiple Robots based on Swarm AI”, 2019.

[13] S.A. Mantserov et K.V. Ilichev, “Group Robotic Platform Based on Mechanisms of Swarm Intelligence”, 2018.