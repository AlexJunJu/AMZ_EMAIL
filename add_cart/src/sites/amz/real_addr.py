import random

real_address = [
    {
        'address_line1': '45 Joe Williams Road',
        'address_line2': '',
        'city': 'Moodus',
        'state': 'CT',
        'zipCode': '06469',
    },
    {
        'address_line1': '73 Clark Gate Road',
        'address_line2': '',
        'city': 'Moodus',
        'state': 'CT',
        'zipCode': '06469',
    },
    {
        'address_line1': '15 School Drive',
        'address_line2': '',
        'city': 'Moodus',
        'state': 'CT',
        'zipCode': '06469',
    },
    {
        'address_line1': '1 Plains Road',
        'address_line2': '',
        'city': 'Moodus',
        'state': 'CT',
        'zipCode': '06469',
    },
    {
        'address_line1': '1 Plains Road',
        'address_line2': '',
        'city': 'Moodus',
        'state': 'CT',
        'zipCode': '06469',
    },
    {
        'address_line1': '6 Main Street',
        'address_line2': '',
        'city': 'East Haddam',
        'state': 'CT',
        'zipCode': '06423',
    },
    {
        'address_line1': '488 Town Stree',
        'address_line2': '',
        'city': 'East Haddam',
        'state': 'CT',
        'zipCode': '06423',
    },
    {
        'address_line1': 'Route 149 (Falls Road)',
        'address_line2': '',
        'city': 'East Haddam',
        'state': 'CT',
        'zipCode': '06423',
    },
    {
        'address_line1': '1330 E 1st St.',
        'address_line2': '',
        'city': 'Santa Ana',
        'state': 'CA',
        'zipCode': '92701',
    },
    {
        'address_line1': '773 Station St.',
        'address_line2': '',
        'city': 'Herndon',
        'state': 'VA',
        'zipCode': '20170',
    },
    {
        'address_line1': '847 Station St.',
        'address_line2': '',
        'city': 'Herndon',
        'state': 'VA',
        'zipCode': '20170',
    },
    {
        'address_line1': '1821 Bella Lago Dr',
        'address_line2': '',
        'city': 'Stockton',
        'state': 'CA',
        'zipCode': '95219',
    },
    {
        'address_line1': '5385 Buford Hwy NE',
        'address_line2': '',
        'city': 'Atlanta',
        'state': 'GA',
        'zipCode': '30340',
    },
    {
        'address_line1': '197 N. Main St.',
        'address_line2': '',
        'city': 'Ellijay',
        'state': 'GA',
        'zipCode': '30540',
    },
    {
        'address_line1': '140 S. Cache, P.O. Box 1212',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '201 North Wolcott',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1930'
    },
    {
        'address_line1': '10875 South US Highway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '204 East 22nd Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2515 Warren Avenue, Suite 450, P.O. Box 1347',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-1347'
    },
    {
        'address_line1': '208 Garfield Street, Suite 200 A',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': 'Ninth and Maple, P.O. Drawer 189',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '204 East 22nd Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '931 Rumsey Avenue, P.O. Box 550',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-0550'
    },
    {
        'address_line1': '515 Ivinson Avenue, P.O. Box 971',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82073-0971'
    },
    {
        'address_line1': '1135 14th Street, P.O. Box 490',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '702 Randall Avenue, P.O. Box 748',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-0748'
    },
    {
        'address_line1': '20 East Simpson Avenue, P.O. Box 3890',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '222 E Garfield St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '284 E Main St',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '637 Front St #1',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '319 S Gillette Ave #110',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '405 W Boxelder Rd #C9',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '102 N 2nd St',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1510 Dewar Dr',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '2441 Foothill Blvd',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '111 W 2nd St #303',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '123 W 1st St #215',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '3000 Central Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '708 Cottonwood Dr',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2020 Carey Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1015 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '112 Center St',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '135 N Main St',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '3904 Central Ave #B',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '120 E Pearl Ave',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1800 Capitol Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '100 E 4th St',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '1008 13th St #C',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '200 S Center St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '200 W 17th St #100',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1321 Sheridan Ave',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '136 W Collins Dr',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '146 S Main St',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '155 W Pearl Ave',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1723 Thomes Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2008 Main St',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '209 W Main St',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '212 9th St',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '2547 E 3rd St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '313 S 2nd St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '320 S Federal Blvd',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '410 E Lyons St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '439 Prairieview Dr #B',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '625 N Washington St',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '819 W Spruce St',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '111 S 7th St',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '401 W 19th St',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '970 W Broadway #B',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1507 8th St',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '245 E 1st St',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '123 W 1st St #100',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '104 S Wolcott St #740',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '401 W 19th St #300',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '5801 Yellowstone Rd #300',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '123 W 1st St #675',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '322 Walnut',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1800 Carey Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '410 E Lyons St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '2020 E Grand Ave',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '1826 18th St',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '222 S Gillette Ave #600',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '222 E 25th St',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '904 S Center St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '800 Werner Ct #350',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '51 Coffeen Ave #102',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '33 N 6th St',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426'
    },
    {
        'address_line1': '123 W 1st St #C91',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '75 E Kelly Ave',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '290 Valley Dr',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '2820 Foothill Blvd #104',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '755 N 4th St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '770 W Collins Dr',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '120 S Durbin St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '21 E Works St',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '308 E Main St',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '933 W Main St',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '1701 Capitol Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1701 Capitol Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '234 E 1st St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1220 Sunshine Ave',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '400 E 1st St',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '20 Wapiti Dr',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '124 N 3rd St',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1069 N 18th St',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '200 W 17th St',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1701 Capitol Ave',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2301 Central Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '200 W 24th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '816 N Federal Boulevard',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '412 S Gillette Avenue',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '310 W 19th Street #200',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1002 S 3rd Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '120 W 1st Street #305',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1349 Sheridan Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '2020 Carey Avenue #3',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '203 S Main Street #3500',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '215 W Buffalo Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '219 E Pine Street #106',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '225 9th Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '406 S 21st Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '50 E Loucks Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': 'Uw Annex Building',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '550 Cache Creek Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '3920 Dorset Court',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '224 S Park Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '801 E 8th Street',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '110 E 2nd',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '410 E Grand Avenue',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': 'Family History Cente',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '518 S 4',
        'address_line2': '',
        'city': ' Glenrock',
        'state': ' WY',
        'zipCode': ' 82637'
    },
    {
        'address_line1': '1240 Front Street',
        'address_line2': '',
        'city': ' Clearmont',
        'state': ' WY',
        'zipCode': ' 82835'
    },
    {
        'address_line1': '300 E Walnut Street',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '60 Spruce Street',
        'address_line2': '',
        'city': ' Granger',
        'state': ' WY',
        'zipCode': ' 82934'
    },
    {
        'address_line1': '112 Main',
        'address_line2': '',
        'city': ' Burns',
        'state': ' WY',
        'zipCode': ' 82053'
    },
    {
        'address_line1': '2800 Central Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '425 Morgan Avenue',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': '322 2nd Street',
        'address_line2': '',
        'city': ' Mountain View',
        'state': ' WY',
        'zipCode': ' 82939'
    },
    {
        'address_line1': '2000 Airport Road',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '2000 Airport Road',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '2360 E Pershing Boulevard',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '205 N Jean',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1898 Fort Road',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': 'Engineering Building',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': 'Law Building',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '105 Wright Boulevard',
        'address_line2': '',
        'city': ' Wright',
        'state': ' WY',
        'zipCode': ' 82732'
    },
    {
        'address_line1': '526 SWeetwater Circle',
        'address_line2': '',
        'city': ' Wright',
        'state': ' WY',
        'zipCode': ' 82732'
    },
    {
        'address_line1': '100 W B Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '30 N Gould Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1808 Sheridan Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '515 N Cache Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '110 E Karns Avenue',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '210 Us Highway 20 S #5',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '335 N Cache Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '335 N Cache Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': 'Po Box 10940',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '1301 Rawhide Drive',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '4100 Sweetbriar Street #103',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1807 Echeta Road',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '3048 Herrington Drive',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1527 18th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '124 E Ramshorn Street',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '124 Ramshorn',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '332 Meadow Drive',
        'address_line2': '',
        'city': ' Alpine',
        'state': ' WY',
        'zipCode': ' 83128'
    },
    {
        'address_line1': '620 Cache Creek Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '128 N Center Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '4100 SWeetbriar Street 103',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1704 N Main Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '444 S Center Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '501 W Lakeway Road',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '3600 Southpark Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '450 N 30th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '500 N 4th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '692 Main Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '301 N Platte Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '520 Creek Avenue',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '309 W Lakeway Road',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '582 E Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '623 W Main Street',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '505 N Center Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '100 N Ash Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1133 W 27th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '490 Fort Street',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '604 N Higley Boulevard',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '112 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '2000 Skyview Drive',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '5225 Yellowstone Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '315 N 4th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '1134 13th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '906 E 2nd Street',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '200 Main Street',
        'address_line2': '',
        'city': ' Lingle',
        'state': ' WY',
        'zipCode': ' 82223'
    },
    {
        'address_line1': '1190 Highway 191',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '408 Broadway Street',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '889 Fort Street',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '3310 Ridge Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '204 W Converse',
        'address_line2': '',
        'city': ' Moorcroft',
        'state': ' WY',
        'zipCode': ' 82721'
    },
    {
        'address_line1': '3806 Dell Range Boulevard',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '867 N 3rd Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '1812 E Richards Street',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '2121 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '4255 S Us Highway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1101 W Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1801 17th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '1103 E Pershing Boulevard',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '425 N Broadway Avenue',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '2801 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1180 Oildale',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636'
    },
    {
        'address_line1': '1202 Main Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '323 E Center Street',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '840 W Main Street',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '621 W Spruce Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '302 E 2nd Street',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '855 E Snow King Avenue',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '200 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '840 Cy Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '715 10th Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '702 E 2',
        'address_line2': '',
        'city': ' Shoshoni',
        'state': ' WY',
        'zipCode': ' 82649'
    },
    {
        'address_line1': '4241 E 2nd Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '601 N 10th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '107 S 7th Street E',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '500 S 6th Street',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '1925 Harrison Drive',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '115 S Main Street',
        'address_line2': '',
        'city': ' Lusk',
        'state': ' WY',
        'zipCode': ' 82225'
    },
    {
        'address_line1': '777 Uinta Drive',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '2701 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '405 Main Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '1711 W Spruce Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '3206 E Grand Avenue',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '1618 Stillwater Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '2305 E 12th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '1660 N 4th Street #A',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '511 N Main Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1107 N Durbin Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1111 Dunn Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '385 Main Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '341 E Pine Street',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '150 N Penland Street',
        'address_line2': '',
        'city': ' Baggs',
        'state': ' WY',
        'zipCode': ' 82321'
    },
    {
        'address_line1': '600 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': 'Route 3',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '832 W Broadway Avenue',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1030 W Collins Drive',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '2334 16th Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '904 W Spruce Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '121 N Broadway Avenue',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '207 S By-Pass Road',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '2105 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '310 S 5th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '1820 17th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '709 N Federal Boulevard',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '103 E Broadway Street',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '105 E Clark Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '908 E Cedar Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '1500 E Valley Road',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '622 State Highway 89 N',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '105 Yellow Creek Road',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '5755 W Highway 22',
        'address_line2': '',
        'city': ' Wilson',
        'state': ' WY',
        'zipCode': ' 83014'
    },
    {
        'address_line1': '1602 Spring Creek Drive',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '675 S Walnut Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1117 Yellowstone Highway',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '4330 E Yellowstone Highway',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '2146 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '102 Reliance Road',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '315 Railway Plaza',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '532 10th Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '520 S Highway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '3200 W McCollister Drive',
        'address_line2': '',
        'city': ' Teton Village',
        'state': ' WY',
        'zipCode': ' 83025'
    },
    {
        'address_line1': '1501 W 2nd Street',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '614 S Greeley Highway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '614 S Greeley Highway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '1538 Main Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '6001 Yellowstone Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '1504 S 1',
        'address_line2': '',
        'city': ' Saratoga',
        'state': ' WY',
        'zipCode': ' 82331'
    },
    {
        'address_line1': '215 N Main Street',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '475 N Cache Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '334 S Fillmore Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '217 Yellowstone Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '747 E E Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': 'The Aspens',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '116 N Front',
        'address_line2': '',
        'city': ' Big Piney',
        'state': ' WY',
        'zipCode': ' 83113'
    },
    {
        'address_line1': '110 Uinta Drive',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '5100 Cy Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '301 E 16th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '113 S Bent Street',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '500 W Main Street',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '1205 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '1205 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '1205 S',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1907 Big Horn Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '195 W Main Street',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '404 S 4th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '301 Platte Avenue',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': '1553 S Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '540 1st Avenue S',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426'
    },
    {
        'address_line1': '2228 Grand Avenue',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '524 Front Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '3806 Dell Range Boulevard #B4',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '86336 Us Highway 89',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '323 Center Street',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1334 S Ash Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '221 N 10th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '1424 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '737 E 2nd Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '3285 W Mccollister Drive',
        'address_line2': '',
        'city': ' Teton Village',
        'state': ' WY',
        'zipCode': ' 83025'
    },
    {
        'address_line1': '525 SW Wyoming Boulevard',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': '1335 S Mckinley Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '832 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '101 N 10th Street',
        'address_line2': '',
        'city': ' Sinclair',
        'state': ' WY',
        'zipCode': ' 82334'
    },
    {
        'address_line1': '404 Highway 414 N',
        'address_line2': '',
        'city': ' Mountain View',
        'state': ' WY',
        'zipCode': ' 82939'
    },
    {
        'address_line1': '4330 W Yellowstone Highway',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636'
    },
    {
        'address_line1': '4025 W Lake Creek Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '116 N Front Street',
        'address_line2': '',
        'city': ' Big Piney',
        'state': ' WY',
        'zipCode': ' 83113'
    },
    {
        'address_line1': '1467 Broadway Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '251 E Main Street',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '1110 Beck Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '323 Winkelman Avenue',
        'address_line2': '',
        'city': ' Big Piney',
        'state': ' WY',
        'zipCode': ' 83113'
    },
    {
        'address_line1': '309 Arapahoe Street',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '138 S Kimball Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '900 N Center Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '50 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '510 W 20th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2706 E Pershing Boulevard',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '145 W Deloney Avenue',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '50 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '4770 Us Highway 26/85',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '600 Fairground Road',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '2426 Higby Road',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '626 W Valley Road',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': 'Highway 26 W',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '606 Lyons Valley Road',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '1114 Sybille Creek Road',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': 'HC 74 Box 355',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '244 El Rancho Road',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '4932 Road 74',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '4750 USHighway 26/85',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': 'Route 3 Box 12b',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': 'Smiths Fork',
        'address_line2': '',
        'city': ' Cokeville',
        'state': ' WY',
        'zipCode': ' 83114'
    },
    {
        'address_line1': 'Po Box 247',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '4740 King Arthur Way',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '5534 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '1205 Hillcrest Drive',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '1608 Pine Street',
        'address_line2': '',
        'city': ' Upton',
        'state': ' WY',
        'zipCode': ' 82730'
    },
    {
        'address_line1': '8420 Us Highway 14',
        'address_line2': '',
        'city': ' Ranchester',
        'state': ' WY',
        'zipCode': ' 82839'
    },
    {
        'address_line1': '3000 W Big Trail Drive',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '2424 Pioneer Avenue #204',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1508 Stillwater Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '970 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '16 Bar X Road',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '12 S 1st Street',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '1807 Capitol Avenue #101j',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': 'Highway 30',
        'address_line2': '',
        'city': ' Hanna',
        'state': ' WY',
        'zipCode': ' 82327'
    },
    {
        'address_line1': '400 S Gillette Avenue #108',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '1702 State Street',
        'address_line2': '',
        'city': ' Meeteetse',
        'state': ' WY',
        'zipCode': ' 82433'
    },
    {
        'address_line1': '3742 Highway 120',
        'address_line2': '',
        'city': ' Meeteetse',
        'state': ' WY',
        'zipCode': ' 82433'
    },
    {
        'address_line1': '602 S 4th Street',
        'address_line2': '',
        'city': ' Basin',
        'state': ' WY',
        'zipCode': ' 82410'
    },
    {
        'address_line1': '890 Highway 20 S',
        'address_line2': '',
        'city': ' Basin',
        'state': ' WY',
        'zipCode': ' 82410'
    },
    {
        'address_line1': '507 Ash Street',
        'address_line2': '',
        'city': ' Frannie',
        'state': ' WY',
        'zipCode': ' 82423'
    },
    {
        'address_line1': '116 E Main Street',
        'address_line2': '',
        'city': ' Byron',
        'state': ' WY',
        'zipCode': ' 82412'
    },
    {
        'address_line1': '155 N 4th Street',
        'address_line2': '',
        'city': ' Basin',
        'state': ' WY',
        'zipCode': ' 82410'
    },
    {
        'address_line1': '1801 Highway 310',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '1916 State Street',
        'address_line2': '',
        'city': ' Meeteetse',
        'state': ' WY',
        'zipCode': ' 82433'
    },
    {
        'address_line1': '1935 State Street',
        'address_line2': '',
        'city': ' Meeteetse',
        'state': ' WY',
        'zipCode': ' 82433'
    },
    {
        'address_line1': '20 Highway 14a E',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '314 W Highway 20 S',
        'address_line2': '',
        'city': ' Manderson',
        'state': ' WY',
        'zipCode': ' 82432'
    },
    {
        'address_line1': '605 E Main Street',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '310 E 1st Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '130 S 9th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '180 N Main Street #1',
        'address_line2': '',
        'city': ' Thayne',
        'state': ' WY',
        'zipCode': ' 83127'
    },
    {
        'address_line1': '402 Nolan',
        'address_line2': '',
        'city': ' Kaycee',
        'state': ' WY',
        'zipCode': ' 82639'
    },
    {
        'address_line1': '319 S Main Street',
        'address_line2': '',
        'city': ' Hyattville',
        'state': ' WY',
        'zipCode': ' 82428'
    },
    {
        'address_line1': '401 S Bent Street #4',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '225 2nd Street',
        'address_line2': '',
        'city': ' Chugwater',
        'state': ' WY',
        'zipCode': ' 82210'
    },
    {
        'address_line1': 'Po Box 223',
        'address_line2': '',
        'city': ' Chugwater',
        'state': ' WY',
        'zipCode': ' 82210'
    },
    {
        'address_line1': '1504 S Spruce Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '420 Mitchelson Street',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '516 S Washington Street',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '126 Dump Road',
        'address_line2': '',
        'city': ' Baggs',
        'state': ' WY',
        'zipCode': ' 82321'
    },
    {
        'address_line1': '161 W Brundage Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '220 E 20th Avenue',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '1324 E M Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '4191 USHighway 26/85',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '512 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '901 N Main Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '338 W 14th Street Lower',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '375 N Cheyenne Street',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '505 E Fremont Avenue',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '1849 Cy Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '110 Tabi Drive',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '66 Grass Valley Drive',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '1626 Inverness Boulevard',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '1482 Commerce Drive #C',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '48 S Wheatland Highway',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '1201 S Greeley Highway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '1326 Bonanza Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '594 N Buchanan Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '165 Tweed Lane',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': 'Po Box 123',
        'address_line2': '',
        'city': ' Veteran',
        'state': ' WY',
        'zipCode': ' 82243'
    },
    {
        'address_line1': '4577 Big Chief Road',
        'address_line2': '',
        'city': ' Burns',
        'state': ' WY',
        'zipCode': ' 82053'
    },
    {
        'address_line1': '2726 W B Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '400 W 15th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '6008 Old Yellowstone Highway',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1660 Highway 50',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': 'PO Box 5',
        'address_line2': '',
        'city': ' Daniel',
        'state': ' WY',
        'zipCode': ' 83115'
    },
    {
        'address_line1': '84 5 Mile Road',
        'address_line2': '',
        'city': ' Parkman',
        'state': ' WY',
        'zipCode': ' 82838'
    },
    {
        'address_line1': 'PO Box 200',
        'address_line2': '',
        'city': ' Cora',
        'state': ' WY',
        'zipCode': ' 82925'
    },
    {
        'address_line1': '1128 Road 9',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '670 Highway 120 W',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '3759 Chuck Wagon Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': 'PO Box 2739',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717'
    },
    {
        'address_line1': '1009 Coburn Avenue',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '236 County Road',
        'address_line2': '',
        'city': ' Hulett',
        'state': ' WY',
        'zipCode': ' 82720'
    },
    {
        'address_line1': '33 Cloudland Road',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '341 E Mill Road',
        'address_line2': '',
        'city': ' Alpine',
        'state': ' WY',
        'zipCode': ' 83128'
    },
    {
        'address_line1': '667 W Flint Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '405 W Saratoga Street',
        'address_line2': '',
        'city': ' Saratoga',
        'state': ' WY',
        'zipCode': ' 82331'
    },
    {
        'address_line1': '1301 W Ramshorn',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '4754 Big Horn Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '866 N Washington Street',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '100 S Railway Avenue',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '12 Kyle Drive',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '514 Us Highway 16 E',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '13764 S Us Highway 191',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '816 Aspen Lane',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '3720 Aspen Place',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '518 N Us Highway 14-16',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': 'l211 W. 27th Street P. O. Box 1929',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003'
    },
    {
        'address_line1': '201 W 21st Avenue',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '18 Sawmill Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '75 County Road 2ab',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '48 S 3 E',
        'address_line2': '',
        'city': ' Cowley',
        'state': ' WY',
        'zipCode': ' 82420'
    },
    {
        'address_line1': '10100 USHighway 191',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '181 Y O Ranch Road',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '82121 USHighway 89',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '12 N Pavillion Road',
        'address_line2': '',
        'city': ' Pavillion',
        'state': ' WY',
        'zipCode': ' 82523'
    },
    {
        'address_line1': '1800 N Spirit Dance Road',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '259 W Fremont Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '91 Highway 31',
        'address_line2': '',
        'city': ' Manderson',
        'state': ' WY',
        'zipCode': ' 82432'
    },
    {
        'address_line1': '167 Industrial Site Road',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '1600 Sunset Drive',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '109 Elm',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '4015 Cy Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '5221 Yellowstone Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '204 S 1st',
        'address_line2': '',
        'city': ' Saratoga',
        'state': ' WY',
        'zipCode': ' 82331'
    },
    {
        'address_line1': '110 W Main Street',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '312 E Ramshorn',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '450 N 3rd Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '300 Us Highway 20 N',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '116 Washakie Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '1100 S Pine Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '51 State Highway 112',
        'address_line2': '',
        'city': ' Hulett',
        'state': ' WY',
        'zipCode': ' 82720'
    },
    {
        'address_line1': 'Newcastle Division',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '712 Storey Boulevard',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '626 Shoshone Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '3260 E Nationway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': 'Colorado & Kendrick',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '1010 W Beaver Drive',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '224 W Road',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '1207 Stampede Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '1863 S Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '901 Trona Drive',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '1600 Sinks Canyon Road',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '51 Primrose Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '417 W 8',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '315 Cy Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '701 S 15th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '588 Avenue H',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '1300 W 5th Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '223 E 5th Street',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '5028 Casper Mountain Road',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '2400 S Hickory Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '514 Ramshorn Street',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '516 W Ramshorn Street',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '27 State Highway 335',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '939 W Birch Street',
        'address_line2': '',
        'city': ' Glenrock',
        'state': ' WY',
        'zipCode': ' 82637'
    },
    {
        'address_line1': '49 Straight And Narrow',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '318 E 6th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '19 Winkelman Avenue',
        'address_line2': '',
        'city': ' Big Piney',
        'state': ' WY',
        'zipCode': ' 83113'
    },
    {
        'address_line1': '1200 Fort Street',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '203 W Flying Circle Drive',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '801 S Beverly Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '1906 Garrett Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '275 N Willow Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '750 Seneca Lane',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '606 N 8th Street W',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '70 E 5th Street',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '525 S 6th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '615 N Burritt Avenue',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '288 USHighway 20 S',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '1111 E 22nd Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '8806 Yellowstone Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '1586 E Monroe Avenue',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '115 E Lyons Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '7404 Maria E Lane',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '70 S Willow',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '2021 Warren Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1225 Maple Way',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '1949 Sugarland Drive #220',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '123 W 1st Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '608 E Pershing Avenue',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '170 Star Lane',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1549 Sheridan Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '332 Main Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '1201 W 2',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '421 E Main Street',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '144 E Grinnell Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1201 W Second',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717'
    },
    {
        'address_line1': 'Po Box 3006',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717'
    },
    {
        'address_line1': '421 E Main Street',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '159 N Wolcott Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1211 S Douglas Highway',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '3315 W Mccollister Drive',
        'address_line2': '',
        'city': ' Teton Village',
        'state': ' WY',
        'zipCode': ' 83025'
    },
    {
        'address_line1': '313 W Cedar Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '122 S 8th Street',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '1022 13th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '4311 Dakota Street',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '355 Barn Owl Court',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': 'Parklane #43',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '1905 17th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '1740 Dell Range Boulevard #300',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '65 S Gros Ventre Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '801 E 4th Street #22',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '1810 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1656 Walnut Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '1740 Dell Range Boulevard H',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '1993 Dewar Drive 1',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '3236 Grand Avenue',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '970 W Broadway E',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1108 14th Street',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '301 Thelma Drive',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '325 Front Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '3465 N Pines Way',
        'address_line2': '',
        'city': ' Wilson',
        'state': ' WY',
        'zipCode': ' 83014'
    },
    {
        'address_line1': '51 Coffeen Avenue #101',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1407 Broomtail Trail',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636'
    },
    {
        'address_line1': '3220 Main',
        'address_line2': '',
        'city': ' Carpenter',
        'state': ' WY',
        'zipCode': ' 82054'
    },
    {
        'address_line1': '2140 Kingsboro Road',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '6711 W Yellowstone Highway',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1451 Coates Avenue',
        'address_line2': '',
        'city': ' Burns',
        'state': ' WY',
        'zipCode': ' 82053'
    },
    {
        'address_line1': 'Po Box 1204',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '415 W Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '640 Highway 20',
        'address_line2': '',
        'city': ' Basin',
        'state': ' WY',
        'zipCode': ' 82410'
    },
    {
        'address_line1': '890 S USHighway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1705 High School Road',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '150 Scott Lane',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1936 Main Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '111 S 4 Street',
        'address_line2': '',
        'city': ' Basin',
        'state': ' WY',
        'zipCode': ' 82410'
    },
    {
        'address_line1': '980 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '980 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1605 Pure Gas Road',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '411 S 2nd Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '122 E Cedar Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '1609 Central Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2620 Commercial Way',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '941 Front Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '1930 Sheridan Avenue',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '418 E Grand Avenue',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '309 S Gillette Avenue',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '933 W 14th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '933 W 14th Street 5',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1811 Newport Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '1912 Capitol Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '330 N Glenwood Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1621 Central Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '701 W 58th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1720 Carey Avenue 600',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '350 Red Canyon Road',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '804 17 Mile Road',
        'address_line2': '',
        'city': ' Arapahoe',
        'state': ' WY',
        'zipCode': ' 82510'
    },
    {
        'address_line1': '110 W 2nd Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '721 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '450 Cole Street',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '1271 N 15th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '222 Gateway Boulevard Office',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '143 S Bent Street B',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '1014 W 15th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1111 E Lincolnway #204',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '710 W Main Street',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '4801 E 2nd Street #102',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '2325 E 12th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '2812 Dogwood Avenue',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '2822 Warren Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1719 Logan Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1449 S Mckinley Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '8 S 5th Street',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426'
    },
    {
        'address_line1': '1632 E 2nd Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '601 SE Wyoming Boulevard',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '1021 E Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2203 E Garfield Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '2810 W B Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '409 5th Street',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '180 Center Street',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '3001 Henderson Drive #I',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1103 E Boxelder Road #D',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '215 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '504 S 4th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '705 Garfield Street',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '225 N Main Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '417 W 6th Street',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '1400 Dell Range Boulevard #38',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '2232 Dell Range Boulevard #302',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '2109 Main Street',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '109 M Street',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '1140 Coffeen Avenue',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1316 Big Horn Avenue',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '1404 Hugur Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '2107 E 12th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '128 E Flaming Gorge Way',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '30 N Gould Street',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '5th & Big Horn',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '1921 E 15th Street',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1616 Converse Avenue',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1640 E 2nd Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '202 S 3rd Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '105 4th Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '10 W Broadway',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1001 Front Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '1130 S Us Highway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': 'Po Box 7629',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '1037 Main Street #B',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '2206 Dell Range Boulevard #7',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '109 N 9th Street W',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '818 W 15th Street',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '265 S Montana Avenue',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '823 S Main Street',
        'address_line2': '',
        'city': ' Kemmerer',
        'state': ' WY',
        'zipCode': ' 83101'
    },
    {
        'address_line1': '238 N Main Street 4',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '37 Meadow Drive',
        'address_line2': '',
        'city': ' Lyman',
        'state': ' WY',
        'zipCode': ' 82937'
    },
    {
        'address_line1': '1804 W Spruce Street',
        'address_line2': '',
        'city': ' Rawlins',
        'state': ' WY',
        'zipCode': ' 82301'
    },
    {
        'address_line1': '303 S 17th Street',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '1900 Converse Avenue #A',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '3151 E Nationway #K6',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '302 S Main Street',
        'address_line2': '',
        'city': ' Lusk',
        'state': ' WY',
        'zipCode': ' 82225'
    },
    {
        'address_line1': '618 Barnett Avenue',
        'address_line2': '',
        'city': ' Encampment',
        'state': ' WY',
        'zipCode': ' 82325'
    },
    {
        'address_line1': '1408 S Greeley Highway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '3975 S Us Highway 89',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1912 Whitney Road',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '5309 State Highway 92 #B',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240'
    },
    {
        'address_line1': '180 Mountain Village Road',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '163 N Clark Street',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '167 Twins Spruce Lane',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '1101 Main Street',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '780 Water Treatment Plant Road',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636'
    },
    {
        'address_line1': '2107 N Us Highway 14-16 #A',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '3869 State Highway 374',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '3125 Kent Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9202'
    },
    {
        'address_line1': '7072 Barton Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1890'
    },
    {
        'address_line1': '820 Lough Dr.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-6429'
    },
    {
        'address_line1': 'P.O. Box 1198',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82902-1198'
    },
    {
        'address_line1': '333 N. Main St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '302 A St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': 'P.O. Box 807',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935-0807'
    },
    {
        'address_line1': '1218 Magnolia Dr. N.',
        'address_line2': '',
        'city': ' Wionia',
        'state': ' WY',
        'zipCode': ' 38577'
    },
    {
        'address_line1': 'Box #2118',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003'
    },
    {
        'address_line1': 'P.O. Box 50214',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82605-0214'
    },
    {
        'address_line1': '1836 S. Melrose St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '200 N. Wolcott St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1929'
    },
    {
        'address_line1': '1900 Ratcliff Dr.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-1503'
    },
    {
        'address_line1': '316 W. Idaho St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '825 N. Federal Blvd.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-2961'
    },
    {
        'address_line1': 'P.O. Box 1026',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '820 Adair Ave.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '482 N. First Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2251'
    },
    {
        'address_line1': 'P.O. Box 2571',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': '3289 Prospector Dr.',
        'address_line2': '',
        'city': ' Caspur',
        'state': ' WY',
        'zipCode': ' 82604-2905'
    },
    {
        'address_line1': '206 E. Grand Ave.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070-3640'
    },
    {
        'address_line1': 'P.O. Box 92',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': 'P.O. Box 20106',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-7002'
    },
    {
        'address_line1': '2206D Sheridan Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-3940'
    },
    {
        'address_line1': 'P.O. Box 923',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-0923'
    },
    {
        'address_line1': '430 N. McKinley St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2118'
    },
    {
        'address_line1': '1001 Dunn Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4846'
    },
    {
        'address_line1': '600 E. First St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2657'
    },
    {
        'address_line1': 'P.O. Box 9007',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002-9007'
    },
    {
        'address_line1': '2120 E. Monroe Ave.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-4829'
    },
    {
        'address_line1': '99 Little Warm Springs Estates',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '11 County Rd. 109',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '156 U.S. Hwy. 20 S.',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443-9403'
    },
    {
        'address_line1': '710 Johnson Ave.',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': 'P.O. Box 5088',
        'address_line2': '',
        'city': ' Etna',
        'state': ' WY',
        'zipCode': ' 83118'
    },
    {
        'address_line1': '2018 Coffeen Ave.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '2433 Primrose Lane',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-5607'
    },
    {
        'address_line1': '6727 W. Uranium Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1514'
    },
    {
        'address_line1': '1461 Commerce Dr.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070-7040'
    },
    {
        'address_line1': '6290 I-80 Service Rd.',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '535 W. Yellowstone Hwy., #202, P.O. Box 2875',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82602-2875'
    },
    {
        'address_line1': '17 Smith Fork Way',
        'address_line2': '',
        'city': ' Lyman',
        'state': ' WY',
        'zipCode': ' 82937'
    },
    {
        'address_line1': '144 E. Midwest Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2540'
    },
    {
        'address_line1': '520 W. Cedar St.',
        'address_line2': '',
        'city': ' Rawlings',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '800 S. Industrial Park',
        'address_line2': '',
        'city': ' Yazoo City',
        'state': ' WY',
        'zipCode': ' 39194'
    },
    {
        'address_line1': '317 S. Third St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '3200 Prospector Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2906'
    },
    {
        'address_line1': '518 S. Walnut St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2311'
    },
    {
        'address_line1': 'P.O. Box 2856',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001-2856'
    },
    {
        'address_line1': '1162 Rd. 12',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '305 W. Platte Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': 'P.O. Box 40046',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1046'
    },
    {
        'address_line1': 'P.O. Box 788',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-0788'
    },
    {
        'address_line1': '305 Commerce Dr.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718-8293'
    },
    {
        'address_line1': '5280 Squaw Creek Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '1119 W. 20th St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '515 S. Walnut St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1035 N. Main St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801-3037'
    },
    {
        'address_line1': '141 S. Center St., Suite 302',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2543'
    },
    {
        'address_line1': '1011 E. Hancock St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': 'US Highway 30',
        'address_line2': '',
        'city': ' Hanna',
        'state': ' WY',
        'zipCode': ' 82327-0460'
    },
    {
        'address_line1': '800 Werner Ct.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '745 N. Division St.',
        'address_line2': '',
        'city': ' West Point',
        'state': ' WY',
        'zipCode': ' 39773'
    },
    {
        'address_line1': '1015 E. 14th St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4803'
    },
    {
        'address_line1': '507 Fifth St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-5205'
    },
    {
        'address_line1': '214 E. Main St.',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': 'P.O. Box 67',
        'address_line2': '',
        'city': ' Reliance',
        'state': ' WY',
        'zipCode': ' 82943-0067'
    },
    {
        'address_line1': 'P.O. Box 2947',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644-2947'
    },
    {
        'address_line1': '1290 N. Second St.',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': 'Cty. Rd. 6SS',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '1160 Alpine Lane, Suite 2D',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '111 Big Horn Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1725'
    },
    {
        'address_line1': '7548 Fuller St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1644'
    },
    {
        'address_line1': '672 N. Washington St., P.O. Box 1240',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110-1240'
    },
    {
        'address_line1': '860 College View Dr.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '110 E. Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4568'
    },
    {
        'address_line1': '305 S. Mickelson St., P.O. Box 232',
        'address_line2': '',
        'city': ' Big Piney',
        'state': ' WY',
        'zipCode': ' 83113-0232'
    },
    {
        'address_line1': '825 N. Robertson Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2106'
    },
    {
        'address_line1': '210 US Hwy. 20 S.',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443-9414'
    },
    {
        'address_line1': '244 S. Sixth Ave.',
        'address_line2': '',
        'city': ' Mountain View',
        'state': ' WY',
        'zipCode': ' 82939'
    },
    {
        'address_line1': '1029 Pilot Butte Ave.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-5410'
    },
    {
        'address_line1': '910 Soulsby St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-5000'
    },
    {
        'address_line1': '27852 U.S. Hwy. 189',
        'address_line2': '',
        'city': ' Kemmerer',
        'state': ' WY',
        'zipCode': ' 83101'
    },
    {
        'address_line1': '1108 E. Monroe',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': 'E. Half Mile St.',
        'address_line2': '',
        'city': ' West Point',
        'state': ' WY',
        'zipCode': ' 39773'
    },
    {
        'address_line1': '520 S. Walnut St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2307'
    },
    {
        'address_line1': '6136 Raderville Rte.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '215 E. 21st Ave.',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240-2819'
    },
    {
        'address_line1': '1088 N. Robertson Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2105'
    },
    {
        'address_line1': '7424 W. Sixth Wn Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1834'
    },
    {
        'address_line1': '1259 State Hwy. 89 N.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930-2188'
    },
    {
        'address_line1': '250 Summit Dr.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-3012'
    },
    {
        'address_line1': '7190 W. Derick Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1883'
    },
    {
        'address_line1': '815 S. Railway',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '346 Amoretti St.',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '1033 Arapahoe St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '424 S. Lincoln St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '15 Hwy. 112',
        'address_line2': '',
        'city': ' Hulett',
        'state': ' WY',
        'zipCode': ' 82720-9657'
    },
    {
        'address_line1': '790 Lane 11 1/2',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435-8522'
    },
    {
        'address_line1': '232 Tulip St.',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520-9491'
    },
    {
        'address_line1': 'P.O. Box 1638',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-1638'
    },
    {
        'address_line1': '4976 Paige St., P.O. Box 2590',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644'
    },
    {
        'address_line1': '906 3rd St.',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82730'
    },
    {
        'address_line1': '3429 Cottonwood Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '507 E. Ivinson Ave.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070-3127'
    },
    {
        'address_line1': '7559 W. Yellowstone Hwy.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1629'
    },
    {
        'address_line1': 'P.O. Box 4975',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1126 Alger Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '2206 Sheridan Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '1045 Beaumont Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1275 N. 6 Mile Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2064'
    },
    {
        'address_line1': 'P.O. Box 130',
        'address_line2': '',
        'city': ' Lagrange',
        'state': ' WY',
        'zipCode': ' 82221-0130'
    },
    {
        'address_line1': 'Bettel Dr. & Third St.',
        'address_line2': '',
        'city': ' Hanna',
        'state': ' WY',
        'zipCode': ' 82327-0339'
    },
    {
        'address_line1': '340 W. Dow St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1920 Thomes Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-3542'
    },
    {
        'address_line1': '1213 N. Rawhide Dr.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '740 E. Collins Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2627'
    },
    {
        'address_line1': '521 E. Sixth St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007'
    },
    {
        'address_line1': '4820 Cleveland',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': 'P.O. Box 1738',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '320 W. Seventh',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '1112 W. 11th St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '507 N. Burma Ave.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-2622'
    },
    {
        'address_line1': '1100 S. Pine St., P.O. Box 1288',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82073'
    },
    {
        'address_line1': '600 Industrial Park',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426-0672'
    },
    {
        'address_line1': '520 Date St.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '231 Blackburn Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-8432'
    },
    {
        'address_line1': '1901 Kroe Lane',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '380 E. North St.',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435-2940'
    },
    {
        'address_line1': '83 Lane 16',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9687'
    },
    {
        'address_line1': '28 Wilkens Peak Dr.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '2249 Coffeen Ave.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '160 N. State Hwy. 59',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': 'P.O. Box 3467',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717-3467'
    },
    {
        'address_line1': '2224 W. Bend Ave.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-2242'
    },
    {
        'address_line1': 'P.O. Box 9',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644-0009'
    },
    {
        'address_line1': '923 Grieves Rd.',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701-9504'
    },
    {
        'address_line1': '1122 S. Summit Ave.',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': '341 E. E St., Suite 190',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1984'
    },
    {
        'address_line1': '991 County Rd. 210',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '2945 W. Fifth St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '811 Edwards St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718-6401'
    },
    {
        'address_line1': '330 Trout Peak Dr.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '108 Sweetwater Dr.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '14 Red Fox Dr.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '1875 W. Curtis St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070-8401'
    },
    {
        'address_line1': '1700 Martin Lane',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '6129 Shannon Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '1006 Shoshoni St.',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '190 Lane 550',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443'
    },
    {
        'address_line1': '415 W. Eight',
        'address_line2': '',
        'city': ' Lusk',
        'state': ' WY',
        'zipCode': ' 82225'
    },
    {
        'address_line1': '2526 Mountain View Dr.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-7505'
    },
    {
        'address_line1': 'P.O. Box 1872',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '825 N. Robertson Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2106'
    },
    {
        'address_line1': '2242 N. 6 Mile Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82644-0850'
    },
    {
        'address_line1': '1701 Robertson Ave',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': '6289 I-80 Service Rd.',
        'address_line2': '',
        'city': ' Pine Bluffs',
        'state': ' WY',
        'zipCode': ' 82082'
    },
    {
        'address_line1': '50 Box # 8789',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '400 E. First St., Suite 301',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2561'
    },
    {
        'address_line1': '1207 Alpine Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': 'P.O. Box 57',
        'address_line2': '',
        'city': ' Wilson',
        'state': ' WY',
        'zipCode': ' 83014'
    },
    {
        'address_line1': '611 S. Walsh Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '1302 9th St.',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '550 Lane 8 1/2',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '3414 Polk Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-6028'
    },
    {
        'address_line1': 'P.O. Box 2961',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82602-2961'
    },
    {
        'address_line1': 'P.O. Box 312',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426-0312'
    },
    {
        'address_line1': '4015 W. Lake Creek Dr. N.',
        'address_line2': '',
        'city': ' Wilson',
        'state': ' WY',
        'zipCode': ' 83014'
    },
    {
        'address_line1': 'P.O. Box 194',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717-0194'
    },
    {
        'address_line1': '479 E. Third St.',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '642 S. Federal Blvd.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-4906'
    },
    {
        'address_line1': 'P.O. Box 350',
        'address_line2': '',
        'city': ' Kemmerer',
        'state': ' WY',
        'zipCode': ' 83101-0350'
    },
    {
        'address_line1': '370 S. Bypass Rd.',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': 'Box 462',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941-0462'
    },
    {
        'address_line1': '830 W. Fetterman St.',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '745 Box # 3723',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': 'P.O. Box 727',
        'address_line2': '',
        'city': ' Torrington',
        'state': ' WY',
        'zipCode': ' 82240-0727'
    },
    {
        'address_line1': '1407 Emerson St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': 'P.O. Box 269',
        'address_line2': '',
        'city': ' Farson',
        'state': ' WY',
        'zipCode': ' 82932-0269'
    },
    {
        'address_line1': '110 W. Second St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '450 S. Federal Blvd., Suite A',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '510 N. Railway Ave.',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': 'P.O. Box 1964',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-1964'
    },
    {
        'address_line1': '720 19th St., P.O. Box 1388',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '602 Skyline Rd.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '811 Edwards St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718'
    },
    {
        'address_line1': '309 S. Fourth St., Suite 202',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070-3750'
    },
    {
        'address_line1': '107 Sixth St.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930-3501'
    },
    {
        'address_line1': '3210 Reesy Rd.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9677'
    },
    {
        'address_line1': '548 N. Washington St., P.O. Box 1420',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110-1420'
    },
    {
        'address_line1': '548 N. Washington St.',
        'address_line2': '',
        'city': ' Afton',
        'state': ' WY',
        'zipCode': ' 83110'
    },
    {
        'address_line1': '2631 Echeta Rd.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-3214'
    },
    {
        'address_line1': '601 Pony Express Rd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009-1138'
    },
    {
        'address_line1': 'Box 176',
        'address_line2': '',
        'city': ' Saratoga',
        'state': ' WY',
        'zipCode': ' 82331-0476'
    },
    {
        'address_line1': '1375 Union Dr.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '933 W. 14th St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-3561'
    },
    {
        'address_line1': 'P.O. Box 9218',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '3325 Big Horn Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '217 S. Main St.',
        'address_line2': '',
        'city': ' Yazoo City',
        'state': ' WY',
        'zipCode': ' 39194'
    },
    {
        'address_line1': '1096 Buffalo Rd',
        'address_line2': '',
        'city': ' Woodville',
        'state': ' WY',
        'zipCode': ' 39669'
    },
    {
        'address_line1': '421 Cleveland',
        'address_line2': '',
        'city': ' Sundance',
        'state': ' WY',
        'zipCode': ' 82729'
    },
    {
        'address_line1': '2803 Big Horn Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9249'
    },
    {
        'address_line1': '1975 Old Salt Creek Hwy.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-9673'
    },
    {
        'address_line1': '925 N. Park St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1222'
    },
    {
        'address_line1': '1546 E. Burlington Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2109'
    },
    {
        'address_line1': '435 N. McKinley St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2117'
    },
    {
        'address_line1': '7956 Fuller St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-1330'
    },
    {
        'address_line1': '4113 W. Yellowstone Hwy.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2605'
    },
    {
        'address_line1': '240 N. Elk St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2227'
    },
    {
        'address_line1': '802 E. C St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-2015'
    },
    {
        'address_line1': '254 N. Center',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1927'
    },
    {
        'address_line1': '315 W. Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1945 Schoonover St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718-6905'
    },
    {
        'address_line1': '42 Douglas Dr.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '88 Rd. 2 AB',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '86 Copper Ave.',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636'
    },
    {
        'address_line1': 'P.O. Box 457',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82602-0457'
    },
    {
        'address_line1': 'P.O. Box 2227',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-2227'
    },
    {
        'address_line1': '237 N. Main St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801-3942'
    },
    {
        'address_line1': '400 S. Miller Ave.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-3936'
    },
    {
        'address_line1': '372 W. Lyons St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072-6712'
    },
    {
        'address_line1': '137 Steel Lane, P.O. Box 147',
        'address_line2': '',
        'city': ' Boulder',
        'state': ' WY',
        'zipCode': ' 82923-0147'
    },
    {
        'address_line1': '939 W. Stuart St.',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': 'P.O. Box 4033',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '102 Pinion St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '502 El Camino Rd.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': '553 W. Garfield St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '202 E. Eighth Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-1463'
    },
    {
        'address_line1': '2709 Bent Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-2951'
    },
    {
        'address_line1': '1401 Airport Pkwy.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '1218 E. Pershing Blvd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-3260'
    },
    {
        'address_line1': '1111 E. Lincolnway',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4848'
    },
    {
        'address_line1': '3507 Cottonwood Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-8414'
    },
    {
        'address_line1': '218 Troy Ct.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '363 S. Riverbend Dr.',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1888 Shumway Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '225 Second St.',
        'address_line2': '',
        'city': ' Chugwater',
        'state': ' WY',
        'zipCode': ' 82210'
    },
    {
        'address_line1': '325 Allied Chemical Rd.',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': 'P.O. Box 4980',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1016 E. Lincoln St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-3016'
    },
    {
        'address_line1': '66 W. Angus St.',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834-1829'
    },
    {
        'address_line1': '103 Reed St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-6128'
    },
    {
        'address_line1': '340 W. Main St.',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '455 Montana Ave.',
        'address_line2': '',
        'city': ' Lovell',
        'state': ' WY',
        'zipCode': ' 82431'
    },
    {
        'address_line1': '9 Little Rock Rd.',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435'
    },
    {
        'address_line1': '612 Center St.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930'
    },
    {
        'address_line1': '3802 D Lane',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716'
    },
    {
        'address_line1': 'P.O. Box 1184',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435-1184'
    },
    {
        'address_line1': '1712 Terra Ave.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '9 Goldeneye Dr.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '2130 E. 21st St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': 'P.O. Box 1240',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935-1240'
    },
    {
        'address_line1': '3889 Hwy. 374',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '1058 Colina Dr.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '1321 Magnolia Dr. S',
        'address_line2': '',
        'city': ' Wiggins',
        'state': ' WY',
        'zipCode': ' 39577'
    },
    {
        'address_line1': '1321 Magnolia Dr S',
        'address_line2': '',
        'city': ' Wiggins',
        'state': ' WY',
        'zipCode': ' 39577'
    },
    {
        'address_line1': 'P.O. Box 204',
        'address_line2': '',
        'city': ' Evansville',
        'state': ' WY',
        'zipCode': ' 82636-0204'
    },
    {
        'address_line1': '1814 Central Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-4416'
    },
    {
        'address_line1': 'P.O. Box 757',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-0757'
    },
    {
        'address_line1': '78 Cty. Rd.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414'
    },
    {
        'address_line1': '2824 Big Horn Ave.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9249'
    },
    {
        'address_line1': '2425 Mountain View Dr.',
        'address_line2': '',
        'city': ' Cody',
        'state': ' WY',
        'zipCode': ' 82414-9754'
    },
    {
        'address_line1': '200 Fish Hatchery Rd.',
        'address_line2': '',
        'city': ' Story',
        'state': ' WY',
        'zipCode': ' 82842'
    },
    {
        'address_line1': '350 N. Beech St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': 'P.O. Box 220l Park Dr.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82717-2201'
    },
    {
        'address_line1': '405 Harden Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    },
    {
        'address_line1': '901 Foster Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1640'
    },
    {
        'address_line1': '1322 Randall Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-7209'
    },
    {
        'address_line1': '653 Cy Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-3627'
    },
    {
        'address_line1': 'P.O. Box 4356',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '16th & Gibbon St., P.O. Box 3295',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82071'
    },
    {
        'address_line1': '159 N. Wolcott St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601-1987'
    },
    {
        'address_line1': '3102 White Cloud Rd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-6140'
    },
    {
        'address_line1': '307 1/2 W. Lincoln Way',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4437'
    },
    {
        'address_line1': '3211 Energy Lane',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2941'
    },
    {
        'address_line1': '432 Greybull Ave.',
        'address_line2': '',
        'city': ' Greybull',
        'state': ' WY',
        'zipCode': ' 82426-2037'
    },
    {
        'address_line1': '320 W. 25th St., Suite 340',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-3005'
    },
    {
        'address_line1': '1240 W. Collins Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2800'
    },
    {
        'address_line1': '5838 U.S. Hwy. 26',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': '370 Blairtown Fleming Gorge Rd.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '127 Folsom Dr.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': '84 E. Gatchell St.',
        'address_line2': '',
        'city': ' Buffalo',
        'state': ' WY',
        'zipCode': ' 82834'
    },
    {
        'address_line1': '3219 E. Pershing Blvd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-5769'
    },
    {
        'address_line1': '302 W. Cedar St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': '2023 E. 13th St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-5101'
    },
    {
        'address_line1': 'Hwy. 89',
        'address_line2': '',
        'city': ' Alpine',
        'state': ' WY',
        'zipCode': ' 83128'
    },
    {
        'address_line1': '535 N. Beverly St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609-1768'
    },
    {
        'address_line1': '535 N. Main St.',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801'
    },
    {
        'address_line1': '92 W. Richards St.',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '29 Maiden Rd.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501-8968'
    },
    {
        'address_line1': '330 Banks Rd.',
        'address_line2': '',
        'city': ' Sundance',
        'state': ' WY',
        'zipCode': ' 82729-9554'
    },
    {
        'address_line1': '680 Airfield Lane',
        'address_line2': '',
        'city': ' Sheridan',
        'state': ' WY',
        'zipCode': ' 82801-5837'
    },
    {
        'address_line1': '16 Cimarron Lane',
        'address_line2': '',
        'city': ' Dubois',
        'state': ' WY',
        'zipCode': ' 82513'
    },
    {
        'address_line1': 'P.O. Box 631',
        'address_line2': '',
        'city': ' Kemmerer',
        'state': ' WY',
        'zipCode': ' 83101-0631'
    },
    {
        'address_line1': '33 Bobcat St.',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82072'
    },
    {
        'address_line1': 'P.O. Box 481',
        'address_line2': '',
        'city': ' Mills',
        'state': ' WY',
        'zipCode': ' 82644-0481'
    },
    {
        'address_line1': '1831 Schoonover St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82718-6913'
    },
    {
        'address_line1': '605 E. Seventh St.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-4403'
    },
    {
        'address_line1': '2000 E. F St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '2000 Foothill Blvd.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-5604'
    },
    {
        'address_line1': '209 Limestone Ave.',
        'address_line2': '',
        'city': ' Gillette',
        'state': ' WY',
        'zipCode': ' 82716-3025'
    },
    {
        'address_line1': 'P.O. Box 56',
        'address_line2': '',
        'city': ' Powell',
        'state': ' WY',
        'zipCode': ' 82435-0056'
    },
    {
        'address_line1': '703 S. Fourth Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': '6750 W. Zero Rd.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604-2112'
    },
    {
        'address_line1': '212 Nichols Ave.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '2300 E. Ninth St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': 'P.O. Box 1675',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82073'
    },
    {
        'address_line1': 'P.O. Box 836',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '195 E. Cole Rd.',
        'address_line2': '',
        'city': ' Wheatland',
        'state': ' WY',
        'zipCode': ' 82201'
    },
    {
        'address_line1': '3032 Thomas Rd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82009'
    },
    {
        'address_line1': '7250 Box 2277',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '708 Baldwin Dr.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001'
    },
    {
        'address_line1': '545 S. Fifth St.',
        'address_line2': '',
        'city': ' Thermopolis',
        'state': ' WY',
        'zipCode': ' 82443-3045'
    },
    {
        'address_line1': '1640 Martin Lane',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '1614 E. Fox Farm Rd.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82007-2549'
    },
    {
        'address_line1': '224 N. Ninth St.',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633'
    },
    {
        'address_line1': '1094 W. River Rd.',
        'address_line2': '',
        'city': ' Worland',
        'state': ' WY',
        'zipCode': ' 82401'
    },
    {
        'address_line1': 'P.O. Box 5329',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82003-5329'
    },
    {
        'address_line1': 'P.O. Box 50518',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82605-0518'
    },
    {
        'address_line1': '1344 S. Boxelder St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82604'
    },
    {
        'address_line1': 'P.O. Box 362',
        'address_line2': '',
        'city': ' Baggs',
        'state': ' WY',
        'zipCode': ' 82321-0362'
    },
    {
        'address_line1': '1510 Seymour Ave.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4769'
    },
    {
        'address_line1': '510 E. Main St.',
        'address_line2': '',
        'city': ' Riverton',
        'state': ' WY',
        'zipCode': ' 82501'
    },
    {
        'address_line1': '220 S. Elm',
        'address_line2': '',
        'city': ' Lusk',
        'state': ' WY',
        'zipCode': ' 82225'
    },
    {
        'address_line1': '688 Antelope Dr.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901'
    },
    {
        'address_line1': 'S. of Laramie',
        'address_line2': '',
        'city': ' Laramie',
        'state': ' WY',
        'zipCode': ' 82070'
    },
    {
        'address_line1': '1265 Old River Rd.',
        'address_line2': '',
        'city': ' Yazoo City',
        'state': ' WY',
        'zipCode': ' 39194'
    },
    {
        'address_line1': '915 E. Main St.',
        'address_line2': '',
        'city': ' Lander',
        'state': ' WY',
        'zipCode': ' 82520'
    },
    {
        'address_line1': '117 W. 17th St.',
        'address_line2': '',
        'city': ' Cheyenne',
        'state': ' WY',
        'zipCode': ' 82001-4517'
    },
    {
        'address_line1': '535 W. Yellowstone Hwy.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '26 Box 1010',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83002'
    },
    {
        'address_line1': '941 Magnolia Dr.',
        'address_line2': '',
        'city': ' Wiggins',
        'state': ' WY',
        'zipCode': ' 39577'
    },
    {
        'address_line1': '1024 Center St.',
        'address_line2': '',
        'city': ' Evanston',
        'state': ' WY',
        'zipCode': ' 82930-3433'
    },
    {
        'address_line1': '829 Elk St.',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-4527'
    },
    {
        'address_line1': '2632 Commercial Way',
        'address_line2': '',
        'city': ' Rock Springs',
        'state': ' WY',
        'zipCode': ' 82901-4755'
    },
    {
        'address_line1': '516 N. Franklin Ave.',
        'address_line2': '',
        'city': ' Pinedale',
        'state': ' WY',
        'zipCode': ' 82941'
    },
    {
        'address_line1': '306 State Hwy. 59',
        'address_line2': '',
        'city': ' Douglas',
        'state': ' WY',
        'zipCode': ' 82633-9722'
    },
    {
        'address_line1': '235 W. First St.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82601'
    },
    {
        'address_line1': '1911 W. Main St.',
        'address_line2': '',
        'city': ' Newcastle',
        'state': ' WY',
        'zipCode': ' 82701'
    },
    {
        'address_line1': 'P.O. Box 1771',
        'address_line2': '',
        'city': ' Jackson',
        'state': ' WY',
        'zipCode': ' 83001'
    },
    {
        'address_line1': '400 N. First E. St.',
        'address_line2': '',
        'city': ' Green River',
        'state': ' WY',
        'zipCode': ' 82935'
    },
    {
        'address_line1': '1341 Glenaire Dr.',
        'address_line2': '',
        'city': ' Casper',
        'state': ' WY',
        'zipCode': ' 82609'
    }
]


def get_real_addr():
    return real_address[random.randint(0, len(real_address))]
