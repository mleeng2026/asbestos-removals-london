"""Targeted editorial repair of the 23 short borough pages.

Each entry is authored around a distinct property brief. Shared contact and
survey facts remain shared; no local work history is implied.
"""
from __future__ import annotations

import html as h
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://asbestosremovalsinlondon.co.uk/"

# Heading, three independent situations, specific quote guidance, local links.
PAGES = {
"barking-and-dagenham": (
 "Barking and Dagenham", "A refurbishment finding in Barking, a roof question in Dagenham or work at a managed property in Becontree needs its own scope. Tell us which part of the building is affected and what work is waiting.",
 [
 ("When a Barking refurbishment finds a board", "If an electrician or builder has stopped near Barking station because a panel has been exposed, leave it undisturbed and send the survey page or sample result if one exists. Asbestos AIB removal is assessed differently from asbestos cement sheet removal; a photograph alone cannot establish the material. Tell us whether services are live and whether the room is occupied."),
 ("Dagenham roofs and outbuildings", "For an outbuilding off the A13 or a garage in Dagenham, say whether the quote is for roof sheets, wall panels or the whole structure. Include approximate dimensions, access through the property and any damage or debris. Those details stop a roof-only enquiry being confused with demolition of the garage."),
 ("Becontree and managed homes", "For a landlord or housing manager dealing with several addresses around Becontree, send the relevant survey extract for each property separately. Name the room, the confirmed material and the access contact. We can discuss the programme together while keeping each property's removal scope clear.")],
 "Which address in Barking or Dagenham is affected, what material was identified, and when must the next trade return? If you have no survey yet, call and explain what was found. Start with a free quote or a site visit where the scope needs checking.",
 ["barking","dagenham","becontree"], ["asbestos-aib-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"bexley": (
 "Bexley", "A garage roof in Bexleyheath, floor work in Welling and a commercial brief near Erith call for different information. We cover the borough and can work from an existing survey or help you decide what to check first.",
 [
 ("A garage roof before other building work", "If a roofer is waiting at a Bexleyheath property, tell us whether corrugated sheets are on the garage alone or on an adjoining structure. Photos from ground level, approximate roof dimensions and the survey finding help define asbestos garage roof removal. Do not remove a sample or disturb damaged sheets for the sake of an enquiry."),
 ("Floor tiles in a Welling purchase", "Buying a house around Welling or Sidcup and planning new flooring? A survey may identify floor tiles but say nothing about the adhesive beneath them. Send the exact finding and identify which rooms are in the renovation. We can then discuss asbestos floor tile removal and whether asbestos bitumen adhesive removal is part of the requested work."),
 ("Erith premises and access", "For a unit in Erith, state whether the building is operating, which roof or internal area is affected and how it can be accessed. A roof-sheet enquiry and an internal asbestos AIB removal brief need different planning. Drawings and a refurbishment survey are useful when available; you can contact us before assembling a full pack.")],
 "Send the Bexley postcode, material finding, affected area and next construction stage. Include photos or measurements if safe and available. We can discuss a free quote and whether a visit is needed.",
 ["bexleyheath","welling","erith","sidcup"], ["asbestos-floor-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"brent": (
 "Brent", "If a survey has identified asbestos in a Wembley unit, a Kilburn flat or a Harlesden refurbishment, send the finding and tell us which part of the project is being held up.",
 [
 ("Wembley units and larger roofs", "A business near Wembley Park may need a roof or plant-area item dealt with before fit-out. Identify the exact roof bay or room, whether operations continue below, and the confirmed material. Asbestos roof removal is a different brief from work on insulation or board around services. A roof plan or survey schedule makes the first discussion more useful."),
 ("Kilburn flats and shared space", "In a flat off Kilburn High Road, a survey finding in a service riser or communal corridor affects more than one household's access. Tell us who controls the shared area, whether the item is asbestos insulating board (AIB) or another material, and when the contractor needs to work. We can discuss asbestos AIB removal without assuming a flat-only scope."),
 ("Harlesden flooring before renovation", "For shops or houses around Harlesden station, list the rooms or floor areas being stripped and send the sample result if you have one. Old tiles and black adhesive should not be treated as the same finding automatically. We can quote for asbestos floor tile removal and discuss asbestos bitumen adhesive removal if that material is confirmed too.")],
 "For a Brent free quote, provide the postcode, report page, affected rooms or roof area, photos and any handover date. If the material is still only suspected, call before anyone disturbs it.",
 ["wembley","kilburn","harlesden","willesden"], ["commercial-asbestos-removal-london.html","asbestos-aib-removal-london.html"]),
"bromley": (
 "Bromley", "Need to move a renovation on in Bromley, replace a garage roof in Orpington or assess a finding at a Beckenham property? Tell us what the survey says, or describe what has stopped if there is no report yet.",
 [
 ("Orpington garage roof: roof or whole garage?", "A quote for asbestos garage roof removal near Orpington station needs the roof dimensions and how the sheets can be reached. Say whether the walls and frame stay, whether the sheets are damaged, and if a driveway or narrow side passage is the only access. Removing the whole outbuilding is a separate scope. Photos taken without touching the material can help."),
 ("Beckenham ceiling before plastering", "When plastering or lighting work stops in a Beckenham flat because a textured ceiling is suspected, the first useful distinction is whether asbestos has actually been confirmed by sampling. Send the result if you have it, the room sizes and what finish is planned afterwards. Asbestos Artex removal and asbestos textured coating removal can then be discussed around the actual refurbishment sequence."),
 ("A Bromley town centre property with several findings", "A refurbishment survey for a shop or managed building near Bromley South may list board, floor finishes and pipe insulation in different areas. Send the relevant schedule with item references and access restrictions. Asbestos AIB removal and asbestos pipe lagging removal can involve different controls. We should price the confirmed items and the areas that genuinely need work, rather than assume every entry in a report is for removal.")],
 "For a Bromley quote, send the postcode and survey finding if you have one. Tell us which trade is waiting, the rooms or roof area involved, approximate sizes and when access is possible. You can still call without paperwork.",
 ["bromley","orpington","beckenham","penge"], ["asbestos-artex-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"camden": (
 "Camden", "A flat refurbishment in Kentish Town, service work around Camden Town and a managed building near Hampstead need clear survey references and access details. Tell us what is holding the work up.",
 [
 ("Kentish Town flats and shared routes", "If board is reported beside a riser or above a shared corridor, send the survey's item number and explain who manages that part of the building. Access through occupied flats can affect the programme. Asbestos AIB removal must be assessed from the confirmed material and planned disturbance, not inferred from a photograph of a panel."),
 ("Camden Town shop fit-outs", "For a shop near Camden Town station, identify whether the finding is above a suspended ceiling, behind a display or beneath existing flooring. A fit-out plan and refurbishment survey help link each asbestos item to the area the trades actually need. Tell us when the shop must reopen and whether public access can be kept separate from the work area."),
 ("Hampstead purchase or leak", "When a buyer or owner near Hampstead has a ceiling or floor opened after a leak, describe what was exposed and whether a surveyor has sampled it. Do not lift more flooring just to take photographs. We can discuss asbestos floor tile removal, asbestos textured coating removal or another scope once the material and affected area are clear.")],
 "Send a Camden postcode, the survey or sample page, relevant photos and the part of the building affected. If work has stopped and no test exists, call with the situation first; we can explain the next step.",
 ["camden-town","kentish-town","hampstead","swiss-cottage"], ["asbestos-aib-removal-london.html","asbestos-floor-removal-london.html"]),
"enfield": (
 "Enfield", "A roof near Enfield Town, a floor in Edmonton and a contractor waiting in Palmers Green are separate jobs with separate access needs. Tell us which material was found and what must happen next.",
 [
 ("Enfield Town outbuildings", "For a garage or shed near Enfield Town station, say whether the roof alone is being replaced or the entire building is being cleared. Approximate sheet count or dimensions, a safe exterior photograph and access information help with asbestos garage roof removal. If the roof is broken, mention any loose pieces separately."),
 ("Edmonton commercial units", "A premises near Meridian Water or the A406 may contain asbestos cement sheets on a larger roof, while a service area inside may have different materials. Send drawings or the survey item references and identify the part of the site that must stay in use. The material, height and access decide what further information is needed for a quote."),
 ("Palmers Green refurbishment", "If an electrician near Palmers Green station has stopped after opening a cupboard or ceiling, leave the material alone. A confirmed AIB panel and a textured finish do not call for identical work. Send the survey finding if available, what was opened and whether the room is occupied; we can discuss the appropriate removal scope.")],
 "For an Enfield quote, include postcode, material, approximate amount and whether builders or roofers are waiting. A report helps, but you can contact us before one is available.",
 ["enfield-town","edmonton","palmers-green","southgate"], ["asbestos-garage-roof-removal-in-london.html","commercial-asbestos-removal-london.html"]),
"greenwich": (
 "Greenwich", "If building work has stopped in Woolwich, a landlord needs a floor item removed in Eltham or a roof is being planned near Greenwich, send the survey finding and describe the next trade's work.",
 [
 ("Woolwich plant and service spaces", "A report for a commercial building around Woolwich Arsenal can list insulation, board and cement materials in separate service areas. State the room, item reference and whether building systems must remain live. Asbestos pipe lagging removal is not interchangeable with asbestos cement flue removal; the confirmed finding sets the brief."),
 ("Eltham flooring before new finishes", "In an Eltham house or flat, identify the rooms where the old floor must come up. Send the result for the tiles and, if the adhesive has been tested separately, that finding too. Photos and approximate floor areas help us discuss asbestos floor tile removal without assuming that every dark adhesive contains asbestos."),
 ("Greenwich roof access", "For a garage roof or larger premises around the A2, explain the roof size, height and route for removing sheets. Say whether the building will remain occupied or operational. We can discuss asbestos roof removal from the survey and access information rather than a postcode alone.")],
 "Tell us the Greenwich postcode, confirmed material, affected area and when another trade needs access. If no survey has been done, call with what is visible and the planned work before disturbing it.",
 ["greenwich","woolwich","eltham","plumstead"], ["asbestos-pipe-removal-london.html","asbestos-floor-removal-london.html"]),
"hackney": (
 "Hackney", "A riser finding in a Dalston block, floor work near Hackney Central or a shop refurbishment in Stoke Newington needs more detail than the borough name. Send the finding and tell us who is waiting.",
 [
 ("Dalston blocks and shared services", "If a survey identifies asbestos insulating board around a service riser near Dalston Junction, say which floors and flats need access. Include the building manager's contact and whether the service can be isolated. We can discuss asbestos AIB removal from the specific survey item rather than treating the whole block as one room."),
 ("Hackney Central floors", "For a shop or flat near Hackney Central station, identify the affected rooms, old tiles and any separately confirmed adhesive. A flooring contractor may need one area handed back before another. Send the sample result and approximate square metres so asbestos floor tile removal can be scoped around the actual sequence."),
 ("Stoke Newington ceilings", "If a textured finish is holding up rewiring or plastering, leave it intact while its composition is checked. Tell us whether the work is in one ceiling, several rooms or a communal area. Once a sample or survey has identified the material, we can discuss asbestos Artex removal and access to the occupied property.")],
 "For a Hackney free quote, send the postcode, survey extract or sample result, photos taken safely and the next trade's planned date. Call first if you have no paperwork and work has stopped.",
 ["dalston","hackney-central","stoke-newington","shoreditch"], ["asbestos-aib-removal-london.html","asbestos-artex-removal-london.html"]),
"hammersmith-and-fulham": (
 "Hammersmith and Fulham", "From a Fulham flat to a Hammersmith office or a Shepherd's Bush shop, the useful first question is what the survey found and which space has to be released for the next work.",
 [
 ("Fulham flats with shared access", "A landlord near Fulham Broadway may have a finding in a flat and another in a communal service cupboard. Send separate survey references and explain who controls access to each area. An asbestos AIB removal brief around services needs its own assessment; do not fold it into a ceiling or floor quote without checking the material."),
 ("Hammersmith commercial fit-out", "For an office around Hammersmith Broadway, identify the ceiling voids, partitions or floor areas that contractors will disturb. Send the refurbishment survey and the construction sequence if you have them. Knowing whether the premises remain occupied helps us discuss access, isolation and the next step for confirmed asbestos materials."),
 ("Shepherd's Bush flooring", "If floor tiles have been discovered while a shop is being refitted near Westfield, stop lifting them and send the sample result. Record the approximate area and whether black adhesive is also confirmed. Asbestos floor tile removal and asbestos bitumen adhesive removal should be quoted as the actual requested items, with opening hours and delivery access noted.")],
 "Give us the W or SW postcode, report pages, affected rooms and any access limits. We can discuss a free quote even if you only have photographs and the survey is still being arranged.",
 ["hammersmith","fulham","shepherds-bush","white-city"], ["commercial-asbestos-removal-london.html","asbestos-floor-removal-london.html"]),
"haringey": (
 "Haringey", "If a loft, ceiling or service area has stopped work in Tottenham, Wood Green or Muswell Hill, send the exact survey finding if you have it and explain what the trades need to do next.",
 [
 ("Wood Green shops and upper flats", "In a mixed-use building near Wood Green station, a shop fit-out may sit below occupied flats. Identify the floor, room and survey item, and tell us who controls the shared services. If asbestos insulating board is confirmed, asbestos AIB removal needs to be assessed around the actual work area and access arrangement."),
 ("Tottenham roof or outbuilding", "For a garage or commercial roof around Tottenham Hale, give the approximate size, height and the route to the building. Explain whether the roof sheets alone are to be removed or whether other parts are included. A roofer's start date and photos from a safe position help make asbestos roof removal enquiries useful."),
 ("Muswell Hill ceilings before decorating", "If a textured ceiling is found during an occupied-home refurbishment, describe the rooms and what work is planned. A photograph cannot tell us if the coating contains asbestos. Send any sample result; if there is none, we can discuss the testing step before asbestos Artex removal is priced.")],
 "For a Haringey quote, send the postcode, what has been confirmed, room or roof dimensions and what is delayed. No report yet? Call without disturbing the material further.",
 ["tottenham","wood-green","muswell-hill","crouch-end"], ["asbestos-artex-removal-london.html","asbestos-roof-removal-london.html"]),
"harrow": (
 "Harrow", "A garage in Pinner, a survey finding around Harrow-on-the-Hill or flooring in Wealdstone may need different removal work. Tell us the exact material and the next stage of the project.",
 [
 ("Pinner garage roof replacement", "If roofers are waiting at a Pinner property, send exterior photos, approximate roof dimensions and the survey result if there is one. Say whether the roof is attached to another structure and whether sheets are damaged. Asbestos garage roof removal can then be discussed separately from taking down an entire garage."),
 ("Harrow-on-the-Hill property purchase", "A purchaser may have a survey listing an AIB panel or an old floor finish but no removal plan. Send the relevant pages and explain what renovation is planned, which rooms are involved and when completion is expected. We can help define asbestos AIB removal or asbestos floor tile removal for the items that actually affect the work."),
 ("Wealdstone managed premises", "For a shop, school or managed building around Harrow & Wealdstone station, provide the room names, item references and who can arrange access. Note if occupants remain on site and whether electrical or mechanical systems are involved. A site visit may be useful where the survey description and actual access do not line up.")],
 "Send the Harrow postcode, survey extract, approximate size and timing. If you only have a suspected material, call to explain what was found before anyone cuts or removes it.",
 ["harrow","pinner","wealdstone","stanmore"], ["asbestos-garage-roof-removal-in-london.html","asbestos-aib-removal-london.html"]),
"havering": (
 "Havering", "A roof in Rainham, work at a Romford unit and a house refurbishment in Hornchurch have different access and material questions. Tell us what has been identified and what is waiting.",
 [
 ("Rainham roofs and industrial buildings", "A business near Rainham station or the A13 may need asbestos cement roof sheets removed before repair or redevelopment. Send the roof plan, approximate size and survey findings. State whether operations below continue and whether there are other confirmed asbestos items in the building; those need separate lines in the scope."),
 ("Romford service areas", "If a commercial survey near Romford station finds board or pipe insulation above a ceiling or in a plant space, provide the item reference and which systems need to remain live. Asbestos AIB removal and asbestos pipe lagging removal are different briefs. Access and isolation should be discussed before assuming a removal date."),
 ("Hornchurch garages and houses", "For an outbuilding or a textured ceiling in Hornchurch, describe which part is to be renovated and whether a sample has confirmed asbestos. Photos from a safe position and approximate dimensions help. A garage roof quote should say clearly if the walls and frame will remain.")],
 "For a Havering free quote, send the postcode, report finding and size of the affected area. Mention if roofers, builders or a tenant handover are waiting; call even if the survey is still pending.",
 ["romford","rainham","hornchurch","upminster"], ["asbestos-roof-removal-london.html","asbestos-pipe-removal-london.html"]),
"hillingdon": (
 "Hillingdon", "If flooring is holding up a Uxbridge refurbishment, a garage roof is due for replacement in Ruislip or a commercial site in Hayes has a survey finding, send the relevant details.",
 [
 ("Uxbridge floors and adhesive", "When a flooring contractor near Uxbridge station has stopped, send the sample results for the floor tiles and adhesive as separate findings if both were tested. Identify each room and its approximate area. We can discuss asbestos floor tile removal and asbestos bitumen adhesive removal against the actual scope, without assuming every black layer contains asbestos."),
 ("Ruislip garage roof", "For a Ruislip house, say if the quote is for roof sheets alone or the complete garage. Include exterior photos, rough measurements and whether access is via a narrow side passage or shared drive. A broken sheet or loose fragments should be flagged rather than moved to take a better photograph."),
 ("Hayes warehouses and fit-outs", "A larger premises around Hayes & Harlington may have roof sheets and internal service areas listed in one survey. Tell us which items must be removed for the planned work and which parts of the building stay in use. A roof plan, survey schedule and access contact make a commercial asbestos removal discussion more precise.")],
 "Send an UB postcode, the report page if available, affected areas and timing. You can call without a survey; describe what work stopped and we can explain how to establish the material.",
 ["uxbridge","ruislip","hayes","west-drayton"], ["asbestos-floor-tile-removal-uxbridge.html","commercial-asbestos-removal-london.html"]),
"hounslow": (
 "Hounslow", "A roof near Brentford, floor tiles in Hounslow and a house in Chiswick can all need asbestos removal, but the quote depends on the confirmed material and access.",
 [
 ("Brentford commercial roofs", "For a unit near Brentford station or the Great West Road, give the approximate roof area, height and survey reference. State if the unit remains in use and which roof sections are included. Asbestos cement roof sheets call for different planning from insulation or board inside the building."),
 ("Hounslow flooring before fit-out", "If flooring work has stopped near Hounslow Central, name the rooms, send the tile result and say whether adhesive was sampled separately. Photos and measurements help with asbestos floor tile removal. Tell us if the site needs to reopen to customers or trades by a particular stage."),
 ("Chiswick occupied homes", "For a ceiling or cupboard in a Chiswick home, explain whether the material is confirmed or only suspected and what the builder intended to disturb. A textured coating, AIB panel and cement flue cannot be treated as one material from a photograph. We can discuss testing or removal from the actual finding.")],
 "For a Hounslow quote, send postcode, survey page or safe photos, approximate quantities and any access limits. Builders waiting? Call with the situation now even if paperwork is incomplete.",
 ["hounslow","brentford","chiswick","feltham"], ["asbestos-roof-removal-london.html","asbestos-floor-removal-london.html"]),
"lambeth": (
 "Lambeth", "A refurbishment near Brixton station, an occupied building in Vauxhall and a Streatham garage involve different people and access. Send the finding and say who needs the space next.",
 [
 ("Brixton shops and upper floors", "A shop fit-out below flats near Brixton station may uncover board around a service opening or old floor finishes. Send the refurbishment survey item and say which space the trades will disturb. If asbestos insulating board is confirmed, asbestos AIB removal should be scoped by location and access, including any shared part of the building."),
 ("Vauxhall managed buildings", "For a block near Vauxhall station, identify whether the report concerns a flat, communal corridor or plant room. A manager may need several trades to use the building while work takes place. Item numbers, access contacts and dates help us discuss a workable sequence without pretending the entire report needs removal."),
 ("Streatham outbuildings", "If a garage roof in Streatham is due for replacement, tell us whether the sheets alone are to go and how they can be reached. Approximate dimensions and safe exterior photos are useful. Note any damage or loose material; leave it undisturbed while the scope is assessed.")],
 "For a Lambeth free quote, give the postcode, affected rooms or roof, confirmed material and who manages access. If your survey is still being arranged, call with the planned work.",
 ["brixton","vauxhall","streatham","clapham"], ["asbestos-aib-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"lewisham": (
 "Lewisham", "If a ceiling in Catford, a garage in Sydenham or a managed property near Lewisham station is holding up work, send the confirmed finding if there is one and explain the project stage.",
 [
 ("Catford ceilings and plastering", "If decorators or plasterers have stopped at a Catford house because of a textured ceiling, tell us which rooms are affected and what the sample result says. Asbestos Artex removal can be discussed when the coating is confirmed; a pattern in a photograph does not identify its composition."),
 ("Sydenham garage access", "A garage roof behind a Sydenham terrace may be reached only through a side path or garden. Send rough roof dimensions, exterior photos and whether the walls stay. That distinction matters for asbestos garage roof removal. Mention broken sheets without lifting or sweeping any pieces."),
 ("Lewisham shared services", "For a managed block near Lewisham station, give the survey item, floor and access contact for any riser, cupboard or ceiling void. A confirmed asbestos AIB panel should be considered around the actual services and occupied spaces. Tell us when the next contractor needs that area released.")],
 "Provide the Lewisham postcode, survey or sample page, photos taken safely and the rooms or roof involved. A call is fine if no report exists yet.",
 ["lewisham","catford","sydenham","deptford"], ["asbestos-artex-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"merton": (
 "Merton", "A purchase in Wimbledon, flooring in Mitcham or a refurbishment in Morden needs a clear account of the material and the work planned around it. We cover the borough without treating every property as the same job.",
 [
 ("Wimbledon purchase surveys", "A buyer near Wimbledon station may have a report listing a ceiling coating, board and old floor finish. Send the relevant pages and say which parts are actually due to be disturbed after completion. We can discuss removal items separately; a survey entry by itself does not mean every material must be taken out."),
 ("Mitcham floors and black adhesive", "If a flooring contractor has stopped in a Mitcham flat or shop, identify the rooms and approximate square metres. Provide separate results for tiles and adhesive if available. Asbestos floor tile removal and asbestos bitumen adhesive removal should follow what is confirmed, rather than assume one result covers both layers."),
 ("Morden garages and access", "For an outbuilding near Morden station, state whether the roof alone is being replaced, the whole garage removed or another structure affected. Safe photographs, rough dimensions and the route through the property help define an asbestos garage roof removal enquiry.")],
 "Send an SW or CR postcode, confirmed material, affected areas and the date another trade needs access. You can contact us before sampling; explain what has been found without disturbing it further.",
 ["wimbledon","mitcham","morden","colliers-wood"], ["asbestos-floor-removal-london.html","asbestos-garage-roof-removal-in-london.html"]),
"newham": (
 "Newham", "A Stratford fit-out, Canning Town service area and East Ham house can involve different asbestos materials. Tell us what the survey identifies and which work cannot move forward.",
 [
 ("Stratford offices and shops", "For a fit-out near Stratford station, send the refurbishment survey items that overlap the planned strip-out. Identify the floor, room and building manager. A ceiling void, floor finish and board around a riser may need separate scopes and access arrangements, especially if the rest of the building stays open."),
 ("Canning Town plant rooms", "If a survey near Canning Town identifies pipe insulation or board around services, give the exact material description and say whether plant must remain live. Asbestos pipe lagging removal and asbestos AIB removal require different assessment. A service drawing and access contact can help settle the next step."),
 ("East Ham homes and outbuildings", "A textured ceiling or garage roof in East Ham may be only suspected until sampled. Tell us what the builder planned to do, which rooms or roof sections are affected and whether material is damaged. You can ask for guidance before cutting a ceiling or moving a roof sheet.")],
 "For a Newham quote, send the postcode, report extract, safe photos and approximate sizes. If trades are waiting but there is no survey yet, call and describe the finding.",
 ["stratford","canning-town","east-ham","forest-gate"], ["asbestos-pipe-removal-london.html","commercial-asbestos-removal-london.html"]),
"redbridge": (
 "Redbridge", "From an Ilford ceiling to a Barkingside garage or a Wanstead flat, send what has been found and tell us what work needs the space afterwards.",
 [
 ("Ilford textured ceilings", "When lighting or plastering stops at an Ilford property, identify the rooms and whether sampling has confirmed asbestos in the coating. Asbestos Artex removal can be discussed from the result and area, but appearance alone is not a diagnosis. Tell us if people are living in the property during the work."),
 ("Barkingside roof replacement", "If a roofer is waiting near Barkingside station, specify roof-only or whole-garage removal. Approximate dimensions, a safe external photograph and the route for carrying sheets out help form an asbestos garage roof removal brief. Note damaged sheets without touching them."),
 ("Wanstead purchase or leak", "A flat purchase or water leak in Wanstead may expose flooring, a cupboard lining or another unknown material. Say what has been opened and whether there is a survey or sample result. We can discuss the confirmed removal item or how to establish what the material is before further work.")],
 "Send an IG or E postcode, survey finding where available, photos and the work deadline. If you only know builders have stopped, call with that information first.",
 ["ilford","barkingside","wanstead","woodford"], ["asbestos-artex-removal-ilford.html","asbestos-garage-roof-removal-in-london.html"]),
"southwark": (
 "Southwark", "A Bermondsey unit, Peckham flat and office near London Bridge have different access and occupancy needs. Send the survey finding and say which trade needs to work next.",
 [
 ("Bermondsey commercial spaces", "A warehouse or workshop around Bermondsey station may have roof sheets, internal board or service insulation listed in different parts of a survey. Identify the exact items required for the planned repair or fit-out and whether the premises remain operational. A roof drawing and safe access details help with asbestos roof removal scope."),
 ("Peckham floors in occupied flats", "For flooring work in a Peckham flat, name the rooms and send the tile and adhesive findings separately if both were tested. Say whether residents can remain elsewhere during the work and when the flooring contractor returns. Asbestos floor tile removal should match the confirmed area rather than the whole property by default."),
 ("London Bridge office services", "If contractors have stopped above a ceiling or beside a riser near London Bridge, send the survey item and explain which services are live. Asbestos AIB removal around occupied office areas calls for a specific access plan. Building-manager contact and the fit-out sequence are more useful than a generic quote request.")],
 "For a Southwark free quote, send postcode, item references, affected area, safe photos and access details. No survey yet? Call with the planned disturbance so we can discuss the next check.",
 ["southwark","bermondsey","peckham","dulwich"], ["commercial-asbestos-removal-london.html","asbestos-floor-removal-london.html"]),
"tower-hamlets": (
 "Tower Hamlets", "If an office near Canary Wharf, a flat in Bethnal Green or a Poplar service area has an asbestos finding, tell us the exact room and what is due to be disturbed.",
 [
 ("Canary Wharf office fit-outs", "For a building around Canary Wharf station, send the refurbishment survey item and a drawing marking the part being stripped out. Say whether the rest of the floor stays occupied and who manages access. Board, insulation and old floor finishes need their own confirmed scopes rather than one blanket removal instruction."),
 ("Bethnal Green flats", "If rewiring or plastering has stopped in a Bethnal Green flat, describe the ceiling, wall or cupboard involved and send a sample result if available. A textured coating is not automatically asbestos; asbestos Artex removal can be discussed after confirmation. Mention whether the finding affects shared space or only the flat."),
 ("Poplar risers and plant", "A survey around Poplar may find asbestos insulating board or pipe insulation in a service route. Give the item reference, floor and whether systems remain live. Asbestos AIB removal and asbestos pipe lagging removal need separate consideration. Building access and the contractor's return date help plan the next discussion.")],
 "Send the E postcode, survey pages, affected areas and access contact. If no report exists and work has stopped, call before any further disturbance.",
 ["canary-wharf","bethnal-green","poplar","bow"], ["asbestos-aib-removal-london.html","asbestos-pipe-removal-london.html"]),
"waltham-forest": (
 "Waltham Forest", "A loft or ceiling in Walthamstow, a Chingford garage and a Leyton refurbishment each needs the correct material identified before removal is scoped.",
 [
 ("Walthamstow loft findings", "If a survey in a house near Walthamstow Central finds board or insulation in the loft, send the exact item description and say what roof or electrical work is planned. Photographs from a safe position can help show access, but should not be used to identify the fibre or material. A confirmed asbestos AIB removal job differs from pipe insulation work."),
 ("Chingford garage roofs", "For an outbuilding around Chingford station, provide dimensions, whether the roof alone is going and how sheets can leave the property. Mention broken areas and any linked shed or lean-to. These details help distinguish asbestos garage roof removal from a full structure clearance."),
 ("Leyton flats and floors", "If a flooring contractor in Leyton has stopped at old tiles, send the tile sample result and any separate adhesive result. Specify rooms and approximate sizes, especially if the property is occupied. We can discuss asbestos floor tile removal around the actual renovation sequence.")],
 "For a Waltham Forest quote, send postcode, confirmed result, photos and the next trade's timing. Call even if a survey is not yet available; leave suspected material undisturbed.",
 ["walthamstow","chingford","leyton","leytonstone"], ["asbestos-aib-removal-london.html","asbestos-floor-removal-london.html"]),
"westminster": (
 "Westminster", "A plant-room finding in Paddington, a Mayfair office fit-out and a flat in Marylebone need precise access and survey details. Tell us which part of the work is waiting.",
 [
 ("Paddington plant and service rooms", "For a building near Paddington station, send the item references for any pipe insulation, board or flue material and state whether systems must remain operational. Asbestos pipe lagging removal and asbestos AIB removal cannot be scoped from one general photograph. A manager's access contact and service drawing are useful."),
 ("Mayfair commercial programmes", "If a refurbishment near Bond Street affects several floors, mark the survey items that overlap the fit-out and tell us which areas must be handed back first. Occupied floors, deliveries and other contractors can shape access. We can discuss removal against the actual schedule rather than assume everything listed in the survey is to come out."),
 ("Marylebone flats and communal areas", "A finding in a flat near Marylebone station may differ from one in a shared corridor or riser. Send separate report pages and identify who grants entry to each space. If the work involves a textured ceiling or old floor, give room sizes and any sample result before asking for a removal quote.")],
 "For a Westminster free quote, send postcode, report item, floor or room, access contact and programme date. No survey yet? Call with the planned works and where the suspect material was found.",
 ["westminster","paddington","marylebone","soho"], ["asbestos-pipe-removal-london.html","commercial-asbestos-removal-london.html"]),
}

assert len(PAGES) == 23

FAQ_LOCAL = {
"barking-and-dagenham": [("What if a panel has stopped builders near Barking station?", "Leave it undisturbed. Send the survey page or sample result if you have one, and tell us whether services are live and the room is occupied."),("Can a Dagenham garage roof be quoted separately from the walls?", "Yes. State whether the sheets, wall panels or the entire structure are in the proposed work, with approximate dimensions and access details.")],
"bexley": [("What should I send for a Bexleyheath garage roof?", "Send safe exterior photos, approximate roof dimensions, the survey finding if available and whether an adjoining structure is involved."),("Do floor tiles and adhesive in Welling need separate results?", "They can be different materials. Send the exact findings for each layer if both were tested and identify the rooms being renovated.")],
"brent": [("How do I describe a Wembley commercial roof job?", "Identify the roof bay, approximate area, survey finding and whether business continues beneath it. Mention separate internal findings separately."),("What if a Kilburn riser is in a shared corridor?", "Tell us who manages the shared area, which floors need access and what the survey identifies. A flat-only description may miss the communal scope.")],
"bromley": [("Can I ask for the Orpington garage roof only?", "Yes. Say whether the roof sheets alone are to be removed, give rough dimensions and explain access. Removing the entire garage is a different scope."),("What if a Beckenham textured ceiling has not been tested?", "Describe the rooms and planned plastering or electrical work without disturbing the finish. Sampling may be needed before asbestos textured coating removal can be agreed.")],
"camden": [("Who should arrange access to a Kentish Town riser?", "Tell us who manages the shared space and which flats or floors need access. Include the survey item reference and whether services are live."),("What does a Camden Town shop need to send before fit-out?", "Send the refurbishment survey items for the part being stripped out, a plan if available and the reopening or contractor schedule.")],
"enfield": [("Is an Enfield Town garage roof the same job as demolishing the garage?", "No. Tell us whether the sheets alone or the whole structure are included, with dimensions and safe exterior photographs."),("What if an Edmonton site has both roof sheets and internal asbestos?", "List each survey item separately and identify which areas must remain in use. Roof and internal materials need their own scope.")],
"greenwich": [("What information helps with a Woolwich plant-room finding?", "Send the precise material description and item reference, room and whether services must stay live. Pipe insulation and cement flues are different briefs."),("Can I quote Eltham floor tiles from one sample?", "Send the tile result and any separate adhesive result. Include rooms and approximate areas; do not assume one sample covers every layer.")],
"hackney": [("How is access handled for a Dalston service riser?", "Tell us which floors or flats are involved, who manages access and the exact survey item. The confirmed material determines the removal discussion."),("What should I send for Hackney Central floor work?", "Send results for tiles and adhesive where available, the room areas and when the flooring contractor needs the space back.")],
"hammersmith-and-fulham": [("What if asbestos is listed in both a Fulham flat and communal cupboard?", "Send separate item references and identify who grants access to each area. They should not be folded into one unspecified room quote."),("What helps with a Hammersmith office fit-out quote?", "Send the refurbishment survey, affected floor or rooms and the construction sequence. Say if the building remains occupied.")],
"haringey": [("What if an AIB finding is in a Wood Green shop below flats?", "Send the item reference, exact space and who controls shared services. Occupied areas may affect access planning."),("What should I say about a Tottenham roof?", "Give its approximate size, height, survey finding and whether roof sheets alone are included. Tell us if the premises remain in use.")],
"harrow": [("What details help with a Pinner garage roof quote?", "Send the roof dimensions, safe exterior photos, any survey result and whether another building is attached. Note damage without touching the sheets."),("Can a Harrow purchaser send a survey before deciding on work?", "Yes. Send the relevant items and explain which rooms are to be renovated after completion; not every entry necessarily needs removal.")],
"havering": [("What does a Rainham roof enquiry need?", "Send a roof plan or rough area, height, survey finding and whether the site stays operational. List internal findings separately."),("What if a Romford plant room has several asbestos materials?", "Provide each survey item, its precise location and which systems must remain live. Board and pipe insulation require separate assessment.")],
"hillingdon": [("Are Uxbridge floor tiles and black adhesive one item?", "Not automatically. Send separate test results if available, along with the rooms and approximate areas being stripped."),("Can you quote just a Ruislip garage roof?", "Yes. Specify that the walls and frame stay, give rough dimensions and explain the access route. Mention any broken sheets.")],
"hounslow": [("What helps with a Brentford commercial roof quote?", "Send the survey item, roof area and height, and explain whether the unit remains in use. Include access details."),("What if Hounslow flooring work has stopped?", "Leave suspect layers undisturbed. Send the tile result, any separate adhesive result, affected rooms and the contractor's return date.")],
"lambeth": [("What if asbestos is found in a Brixton shop below flats?", "Send the survey item and exact space, including whether it affects shared services or access to the flats."),("How do I describe a Vauxhall block finding?", "Give the floor and room, item reference, manager's access contact and whether the area is communal or inside a flat.")],
"lewisham": [("Is a Catford textured ceiling necessarily asbestos?", "No. The pattern cannot confirm it. Send a sample result if one exists, with the rooms and the planned plastering or electrical work."),("What details matter for a Sydenham garage behind a house?", "Send rough roof dimensions, safe photos and the route through the property. Say whether the walls and frame are staying.")],
"merton": [("Does a Wimbledon purchase survey mean everything must be removed?", "No. Tell us which items overlap the renovation planned after completion so the requested removal work can be discussed."),("Should Mitcham floor tiles and adhesive be listed separately?", "Yes, where both are confirmed. Send the results, affected rooms and approximate floor areas.")],
"newham": [("What should a Stratford fit-out team send?", "Send the survey items in the strip-out area, floor plans if available and the access contact. Say which parts stay occupied."),("What if Canning Town plant remains live?", "State which systems cannot be isolated and send the exact item reference. Pipe insulation and board need separate consideration.")],
"redbridge": [("Can a picture confirm asbestos in an Ilford textured ceiling?", "No. Send a sample result if available, the rooms affected and what work is planned before asbestos Artex removal is scoped."),("What helps with a Barkingside garage roof quote?", "State roof-only or whole-garage removal, rough measurements, access and any damaged sheets. Do not disturb material to photograph it.")],
"southwark": [("How should a Bermondsey unit list several asbestos findings?", "Give each survey item separately, the area needed for the planned work and whether the unit stays operational."),("What if Peckham flat flooring includes adhesive as well as tiles?", "Send separate findings if available and list the affected rooms. Tell us when occupants and flooring contractors need access.")],
"tower-hamlets": [("What information is needed for a Canary Wharf fit-out?", "Send the refurbishment survey items that overlap the strip-out, a floor plan and the building manager's access arrangements."),("Can a Bethnal Green ceiling be priced from its pattern?", "Its pattern does not prove asbestos. Tell us the rooms and planned work, then send a sample result if one exists.")],
"waltham-forest": [("What if a Walthamstow loft survey names board or insulation?", "Send the exact item description and explain what roof or electrical work is planned. Do not use a photograph alone to identify the material."),("What should I send for a Chingford garage roof?", "Provide rough dimensions, whether the roof alone is going, safe exterior photos and the route for carrying sheets out.")],
"westminster": [("What if Paddington plant-room systems must stay live?", "Send the item references and identify which services remain operational. Board and pipe insulation need distinct assessment."),("Can a Mayfair fit-out be planned floor by floor?", "Tell us which survey items affect each floor and which areas need to be handed back first, including occupied spaces and delivery access.")],
}
assert FAQ_LOCAL.keys() == PAGES.keys()

def esc(s: str) -> str:
    return h.escape(s, quote=True)

def make_sections(name, situations, guidance, slugs, services):
    # The situations are independent buyer briefs, not fabricated completed jobs.
    sections = []
    for i, (title, body) in enumerate(situations):
        sections.append(f'<section class="v3-borough-brief"><div class="frame"><h2>{esc(title)}</h2><p>{esc(body)}</p></div></section>')
    sections.append(f'<section class="v3-borough-next"><div class="frame"><h2>What to send for a {esc(name)} quote</h2><p>{esc(guidance)}</p><p><a href="#quote">Get a free quote</a> or call <a href="tel:+442080880271">020 8088 0271</a>. See <a href="/asbestos-removal-services.html">asbestos removal services</a> and <a href="/locations.html">all London areas</a>.</p><p>Related work: '+ ' · '.join(f'<a href="/{esc(s)}">{esc(s.replace(".html", "").replace("-", " "))}</a>' for s in services)+'</p><p>Nearby places: '+ ' · '.join(f'<a href="/asbestos-removal-{esc(s)}.html">{esc(s.replace("-", " ").title())}</a>' for s in slugs)+'</p></div></section>')
    return ''.join(sections)

def make_faq(key, name, situations, guidance):
    qs = [
      (f"Can I ask about asbestos removal in {name} without a survey?", f"Yes. Call with the postcode, what has been found and which work is waiting. A survey or sample result is useful if you have one; do not disturb suspected material just to get a photograph."),
      (f"What if the material in my {name} property is only suspected?", f"Tell us where it is and what the next trade planned to do. The material may need sampling or a suitable survey before a removal scope can be agreed. Appearance alone cannot confirm asbestos."),
      (f"How do I get a quote for {name}?", guidance),
    ]
    qs.extend(FAQ_LOCAL[key])
    return qs

def replace_once(pattern, replacement, source, label):
    out, n = re.subn(pattern, lambda _: replacement, source, count=1, flags=re.S)
    if n != 1: raise ValueError(f"Expected one {label}, got {n}")
    return out

for key, (name, hero, situations, guidance, slugs, services) in PAGES.items():
    path = ROOT / f'asbestos-removal-{key}-london.html'
    source = path.read_text()
    assert 'v3-borough-brief' not in source, path
    hero_section = re.search(r'<section class="legacy-hero borough-hero">.*?</section>', source, re.S).group()
    hero_section = replace_once(r'(<h1>.*?</h1>)<p>.*?</p>', r'\1<p>'+esc(hero)+'</p>', hero_section, 'hero') if False else re.sub(r'(<h1>.*?</h1>)<p>.*?</p>', lambda m:m.group(1)+'<p>'+esc(hero)+'</p>', hero_section, count=1, flags=re.S)
    hero_section = hero_section.replace('Request a free quote ↓','Free quote ↓').replace(f'prepared for work in {name}', 'with taped access and warning signage')
    source = replace_once(r'<section class="legacy-hero borough-hero">.*?</section>',hero_section,source,'hero section')
    blocks = make_sections(name,situations,guidance,slugs,services)
    source = replace_once(r'<section class="local-area-section">.*?(?=<section class="artex-faq">)',blocks,source,'local section')
    qs = make_faq(key,name,situations,guidance)
    faq_json = json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in qs]},ensure_ascii=False,separators=(',',':'))
    source = replace_once(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>',f'<script type="application/ld+json">{faq_json}</script>',source,'FAQ schema')
    faq_html = '<section class="artex-faq"><div class="frame"><p class="section-label">LOCAL QUESTIONS</p><h2>Questions about asbestos removal in '+esc(name)+'</h2><div class="artex-faq-list">'+''.join('<details><summary>'+esc(q)+'</summary><p>'+esc(a)+'</p></details>' for q,a in qs)+'</div></div></section>'
    source = replace_once(r'<section class="artex-faq">.*?</section>',faq_html,source,'FAQ section')
    source = source.replace('We help with homes, rented properties, shops, offices and larger buildings across the borough.',hero)
    source = source.replace('Asbestos removal enquiries across '+name+' and nearby areas.',hero)
    source = source.replace('Need asbestos removed in '+name+'? Call us and speak to a real person about the job. We help with homes, rented properties, shops, offices and larger buildings across the borough.',hero)
    source = source.replace('alt="Controlled asbestos removal enclosure prepared for work in '+name+'"','alt="Controlled asbestos removal enclosure with taped access and warning signage"')
    source = source.replace('"description":"Need asbestos removed in '+name+'? Call us and speak to a real person about the job. We help with homes, rented properties, shops, offices and larger buildings across the borough."','"description":'+json.dumps(hero,ensure_ascii=False))
    path.write_text(source)
print('Repaired',len(PAGES),'borough pages')
