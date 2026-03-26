from googletrans import Translator

x = Translator()

text1 = input("Enter any sentence: ")
text2 = input("Enter target language (like ta, hi, fr): ")

res = x.translate(text1, dest=text2)

print("The original:", text1)
print("Translated:", res.text)
