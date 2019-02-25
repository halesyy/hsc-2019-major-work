mnot = """
  G H H
/ > J E F J H G E C C C ? > > < < ; ; 9 @ >
H F D D F I I E H J J M
M F H H F E F C @ C F E C E = B
; 9 9 ; 9 1 9 9 ; 9 ; J J
O I J L9 $ B 8 <9 8 > = < ? : 8 / f J C ; H E 8 F! >9 ;61( 60+ : :
"""

conversionClassifier = "! $ % & ' ( ) * + . / 0 1 2 3 4 5 6 7 8 9 : ; < = > ? @ A B C D E F G H I J K L M N O P Q R S T U V W X Y Z [ ] ^ _ ` a b c d e f g h i j k l m n o p q r s t u v w x y z { | } ~ ° ± ² ³ ´ µ ¶ · ¸ ¹ º » ¼ ½ ¾ ¿ À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï  Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß"
conversionClassifier = conversionClassifier.split(' ')

# Converting matrix
converter = {}
for conv, i in zip(conversionClassifier, range(0, len(conversionClassifier))):
    converter["{0}".format(conv)] = i
backConverter = {v: k for k, v in converter.items()}

def verticalStep(v, e, B, G, D, A, E):
    for note in v:
        # large if statement, unclean but I wanna finish this
        note = converter[note]
        if note - 0 < 5:
            tE, tA, tD, tG, tB, te = str(note-0)+"--", "---", "---", "---", "---", "---"
        elif note - 5 < 5:
            tE, tA, tD, tG, tB, te = "---",str(note-5)+"--", "---", "---", "---", "---"
        elif note - 10 < 5:
            tE, tA, tD, tG, tB, te = "---", "---", str(note-10)+"--", "---", "---", "---"
        elif note - 15 < 5:
            tE, tA, tD, tG, tB, te = "---", "---", "---", str(note-15)+"--", "---", "---"
        elif note - 20 < 5:
            tE, tA, tD, tG, tB, te = "---", "---", "---", "---", str(note-20)+"--", "---"
        elif note - 25 < 5:
            tE, tA, tD, tG, tB, te = "---", "---", "---", "---", "---", str(note-25)+"---"
        else:
            tE, tA, tD, tG, tB, te = "---", "---", "---", "---", "---", str(note-25)+"-"

        E += tE
        A += tA
        D += tD
        G += tG
        B += tB
        e += te

    return [e, B, G, D, A, E]

def bar(un_notes):
    e, B, G, D, A, E = "", "", "", "", "", ""
    for v in un_notes.split(' '):
        if len(v) >0 and v[0] == '':
            pass
        elif len(v) == 0:
            pass
        else:
            e, B, G, D, A, E = verticalStep(v, e, B, G, D, A, E)
            # actual horizontal manipulating
    return [e, B, G, D, A, E]

def barFormat(ba):
    return "{0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(ba[0], ba[1], ba[2], ba[3], ba[4], ba[5])



for barNotes in mnot.split("\n"):
    b = bar(barNotes)
    print("{0}\n\n\n".format(barFormat(b)))
    # for notes in bar.split(" "):
    # print("next bar")


# for c in mnot:
#     if c == ' ':
#         continue
#     if c == '\n':
#         print("\n\n")
#     else: print(converter[c])
