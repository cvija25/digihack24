import matplotlib.pyplot as plt

# Data
countries = ['BIH', 'BUG', 'HR', 'GR', 'HUN', 'MK', 'RO', 'SRB']
values = [3, 23, 8, 18, 15, 3, 14, 11]

# Create the histogram

plt.axhline(y=7, color='red', linestyle='--', label='y=7')
plt.bar(countries, values, color='skyblue')
plt.title('Broj tržnih centara sa površinom preko 20 hiljada kvm')
plt.xlabel('Država')
plt.ylabel('Broj tržnih centara')
plt.savefig('histogram.jpg')
plt.show()


