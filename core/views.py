from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Registration
from .serializers import RegistrationSerializer
import feedparser, requests
from bs4 import BeautifulSoup
from .mailing import send_webinar_registration_email


# Static data (can later move to DB if needed)
US_STATES = [
   "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming", "District of Columbia (Washington DC)",
  ]

AFRICAN_COUNTRIES = [
    "Algeria",
    "Angola",
    "Benin",
    "Botswana",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cameroon",
    "Central African Republic",
    "Chad",
    "Comoros",
    "Congo (Brazzaville)",
    "Congo (Kinshasa)",
    "Côte d'Ivoire",
    "Djibouti",
    "Egypt",
    "Equatorial Guinea",
    "Eritrea",
    "Eswatini",
    "Ethiopia",
    "Gabon",
    "Gambia",
    "Ghana",
    "Guinea",
    "Guinea-Bissau",
    "Kenya",
    "Lesotho",
    "Liberia",
    "Libya",
    "Madagascar",
    "Malawi",
    "Mali",
    "Mauritania",
    "Mauritius",
    "Morocco",
    "Mozambique",
    "Namibia",
    "Niger",
    "Nigeria",
    "Rwanda",
    "Sao Tome and Principe",
    "Senegal",
    "Seychelles",
    "Sierra Leone",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Sudan",
    "Tanzania",
    "Togo",
    "Tunisia",
    "Uganda",
    "Zambia",
    "Zimbabwe"
]

# AFRICAN_KEYWORDS = [
#     "Africa", "African", "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso",
#     "Burundi", "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
#     "Congo", "Côte d'Ivoire", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea",
#     "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
#     "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
#     "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria",
#     "Rwanda", "Sao Tome", "Senegal", "Seychelles", "Sierra Leone", "Somalia",
#     "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
#     "Zambia", "Zimbabwe"
# ]

class USStatesAPIView(APIView):
    def get(self, request):
        return Response(US_STATES)

class AfricanCountriesAPIView(APIView):
    def get(self, request):
        return Response(AFRICAN_COUNTRIES)

class RegistrationAPIView(APIView):
    def get(self, request):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            registration = serializer.save()

            # Send confirmation email
            send_webinar_registration_email(registration)

            return Response({"message": "Registration successful!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ReutersAfricaFeed(APIView):

    def get(self, request):
            url = "https://www.africanews.com/feed/rss"
            r = requests.get(url, timeout=10)
            feed = feedparser.parse(r.content)

            def extract_og_image(article_url):
                try:
                    res = requests.get(article_url, timeout=10)
                    soup = BeautifulSoup(res.content, "html.parser")
                    og_image = soup.find("meta", property="og:image")
                    return og_image["content"] if og_image else ""
                except:
                    return ""

            african_keywords = [
                "africa", "nigeria", "ghana", "kenya", "ethiopia", "zimbabwe", "uganda", "south africa",
                "cote d'ivoire", "ivory coast", "tanzania", "rwanda", "mali", "senegal", "algeria", "angola",
                "cameroon", "morocco", "tunisia", "libya", "egypt", "sudan", "namibia", "mozambique",
                "somalia", "botswana", "burundi", "zambia", "sierra leone", "liberia", "gabon", "djibouti",
                "benin", "togo", "lesotho", "malawi", "chad", "gambia", "niger"
            ]

            def is_relevant(entry):
                combined_text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
                return any(country in combined_text for country in african_keywords)

            items = []
            for e in feed.entries[:15]:  # Limit to 15 for performance
                if not is_relevant(e):
                    continue

                article_url = e.get("link")
                image_url = extract_og_image(article_url)

                items.append({
                    "title": e.get("title"),
                    "link": article_url,
                    "published": e.get("published", ""),
                    "author": e.get("author", "Africanews"),
                    "summary": e.get("summary", ""),
                    "image": image_url
                })

            return Response({
                "title": "Africanews RSS with Images",
                "items": items
            })

