dial_codes = [
    (880, 'Bangladesh'),
    (55, 'Brazil'),
    (86, 'China'),
    (91, 'India'),
    (62, 'Indonesia'),
    (81, 'Japan'),
    (234, 'Nigeria'),
    (92, 'Pakistan'),
    (7, 'Russia'),
    (1, 'United States')
]
print(type(dial_codes))


country_dial = {country: code for code, country in dial_codes}
print(type(country_dial))
print(country_dial)

sorted_country_dial = {code: country.upper() for country, code in sorted(country_dial.items())}
print(sorted_country_dial)