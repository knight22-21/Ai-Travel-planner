document.getElementById("travelForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const dest = document.getElementById("destination").value;
  const start = document.getElementById("start_date").value;
  const end = document.getElementById("end_date").value;
  const interests = document.getElementById("interests").value;

  const data = { destination: dest, start_date: start, end_date: end, interests };

  const itineraryRes = await fetch("/api/itinerary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const itineraryData = await itineraryRes.json();
  document.getElementById("itinerary").innerText = itineraryData.itinerary;

  const packingRes = await fetch("/api/packing", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  const packingData = await packingRes.json();
  document.getElementById("packing").innerText = packingData.packing_list;
});
