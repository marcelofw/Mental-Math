#%%
import random

n1 = random.randint(10, 99)
n2 = random.randint(10,99)
resultado_real = n1 * n2

print(f"Quanto é {n1} * {n2}")
resposta = int(input("Sua resposta: "))

if resposta == resultado_real:
    print("Você acertou!")
else:
    print(f"Resposta incorreta. A resposta é {resultado_real}.")



# %%
