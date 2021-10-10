title = "Відеокарта GIGABYTE GeForce RTX 3060 Ti EAGLE OC 8G rev. 2.0 (GV-N306TEAGLE OC-8GD rev. 2.0)"
# vendor_code = title.split()[-1].strip("(").strip(")")
vendor_code = title.split("(")[-1].strip(")")
print(vendor_code)
