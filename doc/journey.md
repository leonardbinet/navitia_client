http://doc.navitia.io/?shell#journeys

?from=2.3749036;48.8467927&to=2.2922926;48.8583736' -H 'Authorization: 3b036afe-0110-4202-b9ed-99718476c2e0'Ó


# Parameters
datetime iso-date-time
20160613T133830

datetime_represents Can be departure or arrival.

If departure, the request will retrieve journeys starting after datetime.
If arrival it will retrieve journeys arriving before datetime. 	departure


Required 	Name 	Type 	Description 	Default value
nop 	from 	id 	The id of the departure of your journey. If none are provided an isochrone is computed 	
nop 	to 	id 	The id of the arrival of your journey. If none are provided an isochrone is computed 	
yep 	datetime 	iso-date-time 	Date and time to go 	
nop 	datetime_represents 	string 	Can be departure or arrival.
If departure, the request will retrieve journeys starting after datetime.
If arrival it will retrieve journeys arriving before datetime. 	departure
nop 	traveler_type 	enum 	Define speeds and accessibility values for different kind of people.
Each profile also automatically determines appropriate first and last section modes to the covered area. Note: this means that you might get car, bike, etc fallback routes even if you set forbidden_uris[]! You can overload all parameters (especially speeds, distances, first and last modes) by setting all of them specifically. We advise that you don’t rely on the traveler_type’s fallback modes (first_section_mode[] and last_section_mode[]) and set them yourself.

enum values:
	standard
nop 	data_freshness 	enum 	Define the freshness of data to use to compute journeys

    realtime
    base_schedule

when using the following parameter “&data_freshness=base_schedule”
you can get disrupted journeys in the response. You can then display the disruption message to the traveler and make a realtime request to get a new undisrupted solution. 	base_schedule
nop 	forbidden_uris[] 	id 	If you want to avoid lines, modes, networks, etc.
Note: the forbidden_uris[] concern only the public transport objects. You can’t for example forbid the use of the bike with them, you have to set the fallback modes for this (first_section_mode[] and last_section_mode[]) 	
nop 	first_section_mode[] 	array of string 	Force the first section mode if the first section is not a public transport one. It takes one the following values: walking, car, bike, bss.
bss stands for bike sharing system.
It’s an array, you can give multiple modes.

Note: choosing bss implicitly allows the walking mode since you might have to walk to the bss station.
Note 2: The parameter is inclusive, not exclusive, so if you want to forbid a mode, you need to add all the other modes.
Eg: If you never want to use a car, you need: first_section_mode[]=walking&first_section_mode[]=bss&first_section_mode[]=bike&last_section_mode[]=walking&last_section_mode[]=bss&last_section_mode[]=bike 	walking
nop 	last_section_mode[] 	array of string 	Same as first_section_mode but for the last section 	walking
Other parameters
Required 	Name 	Type 	Description 	Default value
nop 	max_duration_to_pt 	int 	Maximum allowed duration to reach the public transport.
Use this to limit the walking/biking part.
Unit is seconds 	15*60 s
nop 	walking_speed 	float 	Walking speed for the fallback sections
Speed unit must be in meter/seconds 	1.12 m/s
(4 km/h)
Yes, man, they got the metric system
nop 	bike_speed 	float 	Biking speed for the fallback
Speed unit must be in meter/seconds 	4.1 m/s
(14.7 km/h)
nop 	bss_speed 	float 	Speed while using a bike from a bike sharing system for the fallback sections
Speed unit must be in meter/seconds 	4.1 m/s
(14.7 km/h)
nop 	car_speed 	float 	Driving speed for the fallback sections
Speed unit must be in meter/seconds 	16.8 m/s
(60 km/h)
nop 	min_nb_journeys 	int 	Minimum number of different suggested journeys
More in multiple_journeys 	
nop 	max_nb_journeys 	int 	Maximum number of different suggested journeys
More in multiple_journeys 	
nop 	count 	int 	Fixed number of different journeys
More in multiple_journeys 	
nop 	max_nb_tranfers 	int 	Maximum number of transfers in each journey 	10
nop 	max_duration 	int 	Maximum duration of journeys in secondes. Really useful when computing an isochrone 	10
nop 	disruption_active 	boolean 	For compatibility use only.
If true the algorithm take the disruptions into account, and thus avoid disrupted public transport.
Rq: disruption_active=true = data_freshness=realtime
Use data_freshness parameter instead 	False
nop 	wheelchair 	boolean 	If true the traveler is considered to be using a wheelchair, thus only accessible public transport are used
be warned: many data are currently too faint to provide acceptable answers with this parameter on 	False
nop 	debug 	boolean 	Debug mode
No journeys are filtered in this mode 	False
