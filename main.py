import nltk
import re
from nltk.chat.util import Chat, reflections

class FerreroChatbot:
    def __init__(self):
        self.pairs = [

            [
                r".*(bonjour|salut|coucou|hello|helo|bonjor|hy|hay|bnjr).*",
                ["Bonjour, en quoi puis-je vous aider aujourd'hui?"]
            ],
            # General qst
            [
                r".*(produits|offres|assortiment|produit|offre|assortiments.|prroduit|ofre|asortiments|prooduit|offrre|asortiment).*",
                ["Nous offrons une large gamme de produits tels que Ferrero Rocher, Nutella, Kinder, Tic Tac, Raffaello... Souhaitez-vous des informations spécifiques sur l'un de ces produits ?",
                 "Explorez notre vaste sélection de délices, incluant Ferrero Rocher, Nutella, Kinder, Tic Tac, Raffaello... Quel produit vous intéresse particulièrement ? Pourrions-nous vous fournir des détails spécifiques ?",
                 "Chez nous, vous trouverez des produits variés comme Ferrero Rocher, Nutella, Kinder, Tic Tac, Raffaello... Des questions sur ces articles ? Quels détails spécifiques cherchez-vous ?"]
            ],
            # Détails produits
            [
                r".*(détails sur ferrero rocher|informations sur ferrero rocher|details sur ferrero rocher|information sur ferrero rocher|ferrero rocher|ferero rocher).*",
                ["Ferrero Rocher est une confiserie sphérique composée d'une noisette entière enrobée de chocolat au lait et de noisettes concassées. C'est idéal pour les cadeaux ou comme délices festifs.",]
            ],
            [
                r".*(nutella|informations sur nutella|nutela)",
                ["Nutella est une pâte à tartiner au chocolat et aux noisettes qui peut être utilisée sur des toasts, des crêpes, ou incorporée dans des recettes de desserts. Nutella est appréciée dans le monde entier pour son goût unique.",]
            ],
            [
                r".*(kinder surprise|informations sur kinder surprise).*",
                ["Kinder Surprise est un œuf en chocolat qui contient une petite surprise à l'intérieur, souvent un jouet. Les Kinder Surprises sont particulièrement populaires parmi les enfants et sont vendus dans de nombreux pays, sauf aux États-Unis où ils sont interdits à cause des normes sur les objets non comestibles dans les produits alimentaires.",]
            ],
            [
                r".*(tic tac|informations sur tic tac).*",
                ["Tic Tac est une marque de petites pastilles rafraîchissantes disponibles en plusieurs saveurs, telles que la menthe, l'orange, et la cerise. Elles sont vendues dans de petites boîtes en plastique pratiques pour une consommation en déplacement.",]
            ],
            [
                r".*(kinder joy|informations sur kinder joy).*",
                [
                    "Kinder Joy est un œuf en chocolat qui se divise en deux parties: une contenant une couche de cacao et une couche de lait crémeux, et l'autre contenant un jouet. Kinder Joy est très apprécié pour la surprise et le plaisir qu'il offre aux enfants."]
            ],
            [
                r".*(kinder country|informations sur kinder country).*",
                [
                    "Kinder Country est une barre de chocolat avec des céréales croustillantes intégrées. Elle combine le goût riche du chocolat Kinder avec une texture agréablement croquante, offrant une expérience unique et satisfaisante."]
            ],
            [
                r".*(kinder bueno|informations sur kinder bueno).*",
                [
                    "Kinder Bueno est une barre de chocolat composée de gaufrette légère enrobée de chocolat au lait et fourrée d'une crème aux noisettes. C'est une option de snack doux et croustillant, très populaire pour ses textures et son goût délicieux."]
            ],
            [
                r".*(raffaello|informations sur raffaello).*",
                [
                    "Raffaello est une confiserie créée par Ferrero, composée d'une amande entière entourée de crème, puis enrobée de noix de coco râpée. Ce délice est connu pour sa texture légère et croustillante ainsi que pour son goût rafraîchissant et exotique. Raffaello est souvent apprécié durant les fêtes et les occasions spéciales."]
            ],
            # nutrition
            [
                r".*calories de ferrero rocher.*|.*valeur nutritionnelle de ferrero rocher.*",
                ["Chaque Ferrero Rocher contient environ 73 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit.",]
            ],
            [
                r".*calories de nutella.*|.*valeur nutritionnelle de nutella.*",
                ["Une portion de Nutella (deux cuillères à soupe) contient environ 200 calories, avec des graisses, des glucides et un peu de protéines. Vérifiez l'étiquette du produit pour les détails complets.",]
            ],
            [
                r".*calories de tic tac.*|.*valeur nutritionnelle de tic tac.*",
                [
                    "Chaque pastille de Tic Tac contient moins de 2 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            [
                r".*calories de kinder joy.*|.*valeur nutritionnelle de kinder joy.*",
                [
                    "Un œuf Kinder Joy contient environ 110 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            [
                r".*calories de kinder bueno.*|.*valeur nutritionnelle de kinder bueno.*",
                [
                    "Un Kinder Bueno standard contient environ 122 calories par barre. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            [
                r".*calories de kinder surprise.*|.*valeur nutritionnelle de kinder surprise.*",
                [
                    "Un œuf Kinder Surprise contient environ 110 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            [
                r".*calories de kinder country.*|.*valeur nutritionnelle de kinder country.*",
                [
                    "Une barre Kinder Country contient environ 134 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            [
                r".*calories de raffaello.*|.*valeur nutritionnelle de raffaello.*",
                [
                    "Chaque Raffaello contient environ 61 calories. Pour plus de détails nutritionnels, veuillez consulter l'emballage du produit."]
            ],
            # Histoire
            [
                r".*histoire.*|.*fondation.*",
                ["Ferrero a été fondée en 1946 à Alba, en Italie, par Pietro Ferrero. Depuis, nous sommes devenus l'une des plus grandes entreprises de confiseries au monde.",]
            ],
            [
                r".*histoire de kinder.*|.*fondation de kinder.*",
                [
                    "Kinder a été lancée en 1968 par Ferrero avec l'objectif de créer des produits chocolatés destinés spécifiquement aux enfants, tout en assurant leur apport nutritionnel. Le premier produit, Kinder Chocolate, a rapidement été suivi par de nombreux autres produits aimés à travers le monde."]
            ],
            [
                r".*histoire de tic tac.*|.*fondation de tic tac.*",
                [
                    "Tic Tac a été introduit par Ferrero en 1969. À l'origine nommé 'Refreshing Mints', il a été renommé Tic Tac après le son distinctif des pastilles qui se déplacent dans leur boîte. Ce produit est devenu célèbre pour ses petites pastilles rafraîchissantes offertes dans une variété de saveurs."]
            ],
            [
                r".*histoire de raffaello.*|.*fondation de raffaello.*",
                [
                    "Raffaello a été développé par Ferrero en 1989 et est rapidement devenu populaire pour son mélange unique d'amandes, de crème et de noix de coco. Ce produit se distingue par sa texture légère et son apparence élégante, souvent associée à des célébrations et des moments spéciaux."]
            ],
            # Engagement environnement
            [
                r".*durabilité.*|.*environnement.*",
                ["Ferrero s'engage dans la durabilité à travers diverses initiatives, y compris l'utilisation de cacao et d'huile de palme 100% certifiés durables.",]
            ],
            # Careers
            [
                r".*carrière.*|.*emploi.*|.*travailler.*",
                ["Nous offrons diverses opportunités de carrière dans le monde entier. Visitez notre site web dans la section carrières pour les dernières offres d'emploi.",]
            ],
            # Contact et service client
            [
                r".*contact.*|.*service client.*|.*aide.*",
                ["Vous pouvez contacter notre service clientèle via notre site web ou au numéro de téléphone 123-456-7890 pour toute assistance.",]
            ],
            # Ok
            [
                r".*(ok|oui|yes).*",
                ["D'accord, avez-vous d'autres questions ou y a-t-il autre chose sur lequel je peux vous aider ?",
                 "Parfait ! Comment puis-je vous aider davantage ?",
                 "Merci de votre réponse. Que puis-je faire d'autre pour vous aujourd'hui ?"]
            ],
            # Infos
            [
                r".*(chiffre d'affaires|revenus).*",
                [
                    "Le chiffre d'affaires de Ferrero est de 10.3 milliards d'euros, reflétant notre position forte sur le marché mondial des confiseries. Pour des chiffres précis, veuillez consulter notre dernier rapport annuel disponible sur notre site Web."]
            ],
            [
                r".*(nombre d'employés|effectifs).*",
                [
                    "Ferrero emploie environ 47000 milles à travers le monde, avec des opérations dans de nombreux pays. Le nombre exact d'employés peut varier, mais nous sommes fiers de notre équipe globale et diversifiée. Pour plus d'informations détaillées, veuillez visiter notre site Web ou consulter notre rapport annuel."]
            ],

            # Erreur
            [
                r"(.*)",
                ["Je suis désolé, je n'ai pas compris votre question. Pouvez-vous être plus précis ou reformuler votre demande ?",]
            ],
        ]

    def start_chat(self):
        print("Bonjour ! Je suis le chatbot de Ferrero. Comment puis-je vous aider aujourd'hui ? (Tapez 'quit' pour quitter)")
        chat = Chat(self.pairs)
        chat.converse()

def preprocess_input(input_sentence):
    sentence = input_sentence.lower()
    sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence

if __name__ == "__main__":
    chatbot = FerreroChatbot()
    nltk.chat.util.input = lambda prompt: preprocess_input(input(prompt))
    chatbot.start_chat()
