import re

# Your provided text content
text_content = """Coding assessment input dataPublished using Google DocsReport abuseLearn moreCoding assessment input dataUpdated automatically every 5 minutesThe table below contains the input data needed to solve the coding assessment exercise.x-coordinateCharactery-coordinate27█052█217█644░364█546█12░121█345█185█552█047░152█567█079░115█32░434█318░062░682█016░387░283█377█184█343█142█558█630█566░37█00█423█185█143█215█277█254█013█653█464█652█346█453█366█665█448█464█10█633█65█127█660░382█649░487░137█085░036█160█635█226█640█31█120█459█68█631░14█279░286█235█116░452█448░31█274█253█266█043█357█645█271█682█377█338█130░057█340█549█665█368█665█124█053█631░50█152█186█448█554█365█572█521█442█381█072░673█415█660█075░369█680█036█023░461█629█673█249░523█52░215█146█244░283█640░279░40█258█339░136░433█575░274█42░639█467█614█664█323█050░687░472░044█066░468█038█252█653█516█081█629█569█077█544█154░437░344░478█58░584█02█336█35█515█447█622█210░664█42░077█626█048█67█173█336░585░322█115█021█24░330░634█564█228█020█39█077█078█27█572█125█616░255█373█16░285█217█023░214█462░054░534█465█034█630█18░186█170█654░235░66█124█616█67█63█447░242█46░466░214█278█487░547█422█412█684█616░178█074░14█485█465█685░679░516░50█514█083█025█053█156█641█49█622█566░559█312█058█055█013█046█335█310░054█638░03█361█037█171█065█21█314█180█674█378█353█01█481█341░356█379█379█059█073█518░654░175░478█65█447█529█045█040█424░515█520█274░546░080█322░335█41█014█51█52░555█647█386█566░16█55█221█139█337░20█321█529█170█056█00█077█478█143░539█214█328█679█61█643█457█042█223█664█03█28█035█536█241█524░1"""

coordinates = []

# Parse pattern: number + character + number
pattern = r'(\d+)([█░])(\d+)'
for match in re.finditer(pattern, text_content):
    x = int(match.group(1))
    char = match.group(2)
    y = int(match.group(3))
    coordinates.append((char, x, y))

print(f"Found {len(coordinates)} coordinates")

if coordinates:
    # Determine grid dimensions
    max_x = max(coord[1] for coord in coordinates)
    max_y = max(coord[2] for coord in coordinates)

    print(f"Grid size: {max_x + 1} x {max_y + 1}")

    # Create grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters at their specified positions
    for char, x, y in coordinates:
        grid[y][x] = char

    # Print the grid
    print("\nSecret message:")
    print("=" * 80)
    for row in grid:
        print(''.join(row))
    print("=" * 80)
else:
    print("No coordinates found!")
