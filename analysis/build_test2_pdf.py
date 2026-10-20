"""Build the submission-ready English PDF for Test 2."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "test2-ocean-measurements-and-geostrophic-currents.pdf"
SUMMARY = ROOT / "assets" / "argo" / "test2_argo_geostrophic_summary.json"
FIGURE_VELOCITY = ROOT / "assets" / "argo" / "test2_scs_relative_geostrophic_velocity-en.png"
FIGURE_DENSITY = ROOT / "assets" / "argo" / "argo_scs_density_isobar_section-en.png"

NAVY = colors.HexColor("#071F34")
OCEAN = colors.HexColor("#0B6680")
TEAL = colors.HexColor("#1AA89B")
MINT = colors.HexColor("#E9F6F1")
FOAM = colors.HexColor("#F4FAF8")
SAND = colors.HexColor("#F6F1E7")
CORAL = colors.HexColor("#D66536")
INK = colors.HexColor("#102A3C")
MUTED = colors.HexColor("#4E6972")
LINE = colors.HexColor("#C9DAD8")


def register_fonts() -> None:
    fonts = {
        "Body": "C:/Windows/Fonts/arial.ttf",
        "BodyBold": "C:/Windows/Fonts/arialbd.ttf",
        "BodyItalic": "C:/Windows/Fonts/ariali.ttf",
        "Display": "C:/Windows/Fonts/georgia.ttf",
        "DisplayBold": "C:/Windows/Fonts/georgiab.ttf",
    }
    for name, path in fonts.items():
        pdfmetrics.registerFont(TTFont(name, path))


def styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="DisplayBold", fontSize=27,
            leading=31, textColor=NAVY, alignment=TA_LEFT, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Body", fontSize=11.5,
            leading=17, textColor=MUTED, spaceAfter=18,
        ),
        "kicker": ParagraphStyle(
            "Kicker", parent=base["Normal"], fontName="BodyBold", fontSize=8,
            leading=10, textColor=TEAL, spaceAfter=8, tracking=1.6,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="DisplayBold", fontSize=20,
            leading=24, textColor=NAVY, spaceBefore=4, spaceAfter=11,
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontName="BodyBold", fontSize=12.5,
            leading=15, textColor=OCEAN, spaceBefore=9, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Body", fontSize=9.2,
            leading=13.7, textColor=INK, spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Body", fontSize=7.7,
            leading=10.7, textColor=MUTED, spaceAfter=4,
        ),
        "caption": ParagraphStyle(
            "Caption", parent=base["BodyText"], fontName="Body", fontSize=7.8,
            leading=10.8, textColor=MUTED, spaceBefore=5, spaceAfter=8,
        ),
        "question": ParagraphStyle(
            "Question", parent=base["BodyText"], fontName="Display", fontSize=10.4,
            leading=15.5, textColor=colors.white, spaceAfter=0,
        ),
        "equation": ParagraphStyle(
            "Equation", parent=base["BodyText"], fontName="BodyBold", fontSize=10.4,
            leading=16, textColor=NAVY, alignment=TA_CENTER, spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["BodyText"], fontName="Body", fontSize=8.8,
            leading=13, textColor=INK, leftIndent=13, firstLineIndent=-7, bulletIndent=0, spaceAfter=4,
        ),
        "reference": ParagraphStyle(
            "Reference", parent=base["BodyText"], fontName="Body", fontSize=7.5,
            leading=10.3, textColor=MUTED, leftIndent=14, firstLineIndent=-14, spaceAfter=5,
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def callout(content: list, background=MINT, border=TEAL, pad=10) -> Table:
    table = Table([[content]], colWidths=[172 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.7, border),
        ("LEFTPADDING", (0, 0), (-1, -1), pad),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]))
    return table


def fit_image(path: Path, max_width_mm: float, max_height_mm: float) -> Image:
    from PIL import Image as PILImage

    with PILImage.open(path) as image:
        width_px, height_px = image.size
    scale = min(max_width_mm * mm / width_px, max_height_mm * mm / height_px)
    return Image(str(path), width=width_px * scale, height=height_px * scale)


def page_decor(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 11 * mm, width, 11 * mm, stroke=0, fill=1)
    canvas.setFont("BodyBold", 7.5)
    canvas.setFillColor(colors.white)
    canvas.drawString(19 * mm, height - 7 * mm, "TEST 2  |  PHYSICAL OCEANOGRAPHY")
    canvas.setStrokeColor(LINE)
    canvas.line(19 * mm, 14 * mm, width - 19 * mm, 14 * mm)
    canvas.setFont("Body", 7.3)
    canvas.setFillColor(MUTED)
    canvas.drawString(19 * mm, 9 * mm, "Ocean measurements and geostrophic currents")
    canvas.drawRightString(width - 19 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build() -> None:
    register_fonts()
    s = styles()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    section = summary["section"]

    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4,
        leftMargin=19 * mm, rightMargin=19 * mm,
        topMargin=20 * mm, bottomMargin=19 * mm,
        title="Test 2 - Ocean Measurements and Geostrophic Currents",
        author="Ocean Classroom Notes",
        subject="Submission-ready physical oceanography answer with an Argo case study",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_decor)])

    story = []
    story += [
        Spacer(1, 8 * mm),
        p("PHYSICAL OCEANOGRAPHY COURSE ASSIGNMENT", s["kicker"]),
        p("Ocean Measurements and<br/>Geostrophic Currents", s["title"]),
        p("A layered English response with a reproducible South China Sea Argo case study", s["subtitle"]),
        callout([
            p("THE QUESTION", ParagraphStyle("QK", parent=s["kicker"], textColor=colors.HexColor("#88E2CF"))),
            p(
                "Briefly describe the instruments and methods commonly used to measure ocean temperature, salinity, and currents, and discuss their advantages and limitations. Using the concept of geostrophic balance, explain how horizontal variations in seawater density or sea surface height are related to ocean currents. Discuss the conditions under which geostrophic currents can be inferred from observational data.",
                s["question"],
            ),
        ], background=NAVY, border=NAVY, pad=13),
        Spacer(1, 8 * mm),
        p("Brief answer", s["h1"]),
        p(
            "Temperature and salinity are measured most accurately together with CTDs on ships, autonomous floats, gliders and moorings. XBTs provide rapid temperature profiles, while satellites repeatedly map sea-surface temperature and salinity. Currents are measured directly by current meters, ADCPs, drifters, floats and coastal HF radar, or inferred indirectly from satellite sea-surface height and hydrographic density fields. Each approach trades spatial coverage, vertical resolution, temporal continuity, cost and calibration requirements.",
            s["body"],
        ),
        p(
            "For large-scale, slowly varying flow away from strong friction, the horizontal pressure-gradient force approximately balances Coriolis acceleration. A sea-surface-height slope therefore determines surface geostrophic velocity, while horizontal density differences make pressure gradients vary with depth and determine vertical geostrophic shear. Altimetry can yield absolute surface geostrophic flow when absolute dynamic topography is known. Temperature-salinity profiles yield dynamic-height differences and relative geostrophic flow; they require a reference level or independent velocity to become absolute.",
            s["body"],
        ),
        p(
            "Reliable inference requires a small Rossby number, distance from the equator, weak friction, hydrostatic structure, near-synoptic and spatially adequate sampling, calibrated observations, correct altimetric or hydrographic processing, and removal or separate treatment of tides, inertial motion, Ekman flow and other ageostrophic components.",
            s["body"],
        ),
        Spacer(1, 3 * mm),
        Table(
            [[p("CASE RESULT", s["kicker"]), p("10 dbar relative velocity", s["small"]), p("Reference", s["small"])],
             [p("Six official Argo GDAC profiles, 13-16 March 2017", s["body"]),
              p("-0.492 to +0.195 m s<super>-1</super>", s["body"]), p("700 dbar", s["body"])]],
            colWidths=[91 * mm, 49 * mm, 32 * mm],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), SAND), ("BOX", (0, 0), (-1, -1), .6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), .35, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]),
        ),
        PageBreak(),
        p("1. Instruments and observing methods", s["h1"]),
        p("A measurement is useful only when its sampling scale and error sources match the scientific question.", s["subtitle"]),
    ]

    instrument_data = [
        [p("Variable and method", s["small"]), p("Advantages", s["small"]), p("Limitations", s["small"])],
        [p("<b>Temperature: ship CTD / thermistor</b><br/>In situ temperature against pressure, usually with salinity and bottle samples.", s["small"]), p("High accuracy and vertical resolution; co-located T-S profiles.", s["small"]), p("Ship time is costly; sections are sparse and not perfectly simultaneous.", s["small"])],
        [p("<b>Temperature: XBT</b><br/>Expendable falling probe; depth inferred from fall rate.", s["small"]), p("Fast and inexpensive underway profiles.", s["small"]), p("No salinity; expendable; fall-rate and depth biases require correction.", s["small"])],
        [p("<b>Temperature and salinity: Argo, gliders, moorings</b><br/>Autonomous profiles or fixed time series.", s["small"]), p("Long-duration subsurface sampling in poor weather; broad or sustained coverage.", s["small"]), p("Irregular paths, constrained depths, gaps, drift and delayed calibration.", s["small"])],
        [p("<b>Surface T/S: satellite radiometry</b><br/>Infrared or microwave brightness; L-band for salinity.", s["small"]), p("Frequent, broad to nearly global maps.", s["small"]), p("Surface only; cloud affects infrared; coastal, rain, ice and cold-water errors; needs in situ validation.", s["small"])],
        [p("<b>Salinity: CTD conductivity cell</b><br/>Conductivity plus temperature and pressure converted to Practical Salinity.", s["small"]), p("Accurate paired profiles suitable for density calculation.", s["small"]), p("Indirect measurement; sensor drift and biofouling matter.", s["small"])],
        [p("<b>Salinity: Niskin bottle + salinometer</b><br/>Discrete laboratory sample.", s["small"]), p("High-quality reference and calibration; supports other chemistry.", s["small"]), p("Few depths and stations; sampling and analysis take time.", s["small"])],
        [p("<b>Currents: current meter / ADCP</b><br/>Point velocity or acoustic Doppler profiles in depth bins.", s["small"]), p("High-frequency time series; ADCP resolves multiple depths.", s["small"]), p("Limited range and location; platform motion, heading, sidelobes and scatterers require care.", s["small"])],
        [p("<b>Currents: drifters / floats</b><br/>Lagrangian displacement over time.", s["small"]), p("Tracks water-parcel motion across large distances.", s["small"]), p("Sparse and depth-specific; windage, Stokes drift and imperfect depth following can bias results.", s["small"])],
        [p("<b>Currents: HF radar</b><br/>Coastal radio backscatter maps surface velocity.", s["small"]), p("Repeated two-dimensional coastal maps, often near real time.", s["small"]), p("Coastal range only; geometry, interference and weak signal create gaps.", s["small"])],
        [p("<b>Currents: satellite altimetry</b><br/>Velocity inferred from sea-surface-height gradients.", s["small"]), p("Consistent, repeated, broad-scale coverage.", s["small"]), p("Indirect; mapping smooths small scales; geoid, orbit, tides, atmosphere and ageostrophic motion require treatment.", s["small"])],
    ]
    story += [Table(instrument_data, colWidths=[70 * mm, 50 * mm, 52 * mm], repeatRows=1, style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), .6, LINE), ("INNERGRID", (0, 0), (-1, -1), .35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, FOAM]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ])), PageBreak()]

    story += [
        p("2. Geostrophic balance and observational inference", s["h1"]),
        callout([
            p("Core balance", s["h2"]),
            p("f k x u<sub>g</sub> = -(1/rho<sub>0</sub>) grad<sub>h</sub> p", s["equation"]),
            p("The horizontal pressure-gradient force and Coriolis acceleration are equal and opposite. The geostrophic current runs along pressure contours.", s["body"]),
        ]),
        Spacer(1, 4 * mm),
        p("Sea-surface-height route", s["h2"]),
        p("u<sub>g</sub> = -(g/f) d eta/dy &nbsp;&nbsp;&nbsp;&nbsp; v<sub>g</sub> = (g/f) d eta/dx", s["equation"]),
        p(
            "A tilted sea surface creates a horizontal pressure gradient. In the Northern Hemisphere, higher sea level lies to the right of the geostrophic flow. Satellite altimetry provides sea-level anomaly; absolute surface geostrophic velocity requires absolute dynamic topography, formed from sea-level anomaly plus mean dynamic topography or otherwise referenced to the geoid.",
            s["body"],
        ),
        p("Density and thermal-wind route", s["h2"]),
        p("du<sub>g</sub>/dz = (g/(f rho<sub>0</sub>)) d rho/dy &nbsp;&nbsp;&nbsp;&nbsp; dv<sub>g</sub>/dz = -(g/(f rho<sub>0</sub>)) d rho/dx", s["equation"]),
        p(
            "Temperature and salinity determine seawater density. Under hydrostatic balance, horizontal density contrasts make the pressure gradient vary with depth. Sloping isopycnals therefore determine vertical geostrophic shear. Integrating specific-volume anomaly gives dynamic height; its horizontal difference between stations gives velocity relative to a selected pressure surface.",
            s["body"],
        ),
        p("Worked sign and magnitude check", s["h2"]),
        callout([
            p("At 30 N, a 0.20 m sea-level rise over 100 km gives d eta/dx = 2.0 x 10<super>-6</super>. With f = 7.292 x 10<super>-5</super> s<super>-1</super>, v<sub>g</sub> = 0.269 m s<super>-1</super> northward.", s["body"]),
        ], background=SAND, border=CORAL),
        Spacer(1, 4 * mm),
        p("Conditions required", s["h2"]),
    ]
    conditions = [
        "<b>Rotation dominates:</b> Rossby number Ro = U/(|f|L) is much less than one.",
        "<b>Away from the equator:</b> ordinary geostrophic formulas fail as f approaches zero.",
        "<b>Weak friction:</b> avoid surface and bottom boundary layers and strongly frictional coasts.",
        "<b>Slow evolution:</b> local acceleration, tides and inertial motions must be small or filtered.",
        "<b>Hydrostatic structure:</b> pressure is represented by the weight of overlying water.",
        "<b>Adequate sampling:</b> gradients are spatially resolved and observations are near-synoptic.",
        "<b>Corrected observations:</b> calibrate T-S-p sensors and apply orbit, geoid, tide and atmospheric corrections to altimetry.",
        "<b>Velocity reference:</b> density sections need a level of no motion or an independent ADCP, float or inverse reference for absolute current.",
    ]
    story += [p(f"• {item}", s["bullet"]) for item in conditions]
    story += [PageBreak()]

    story += [
        p("3. South China Sea case study", s["h1"]),
        p("From official Argo profiles to relative geostrophic velocity", s["subtitle"]),
        p(
            "Six single-cycle core profiles were downloaded from the official Coriolis Argo GDAC mirror. The stations span 110.201-115.601 E and 14.002-15.836 N and were sampled from 13 to 16 March 2017. Adjusted pressure, temperature and salinity with Argo QC flags 1 or 2 were preferred, with QC-approved raw values used only as fallback.",
            s["body"],
        ),
        p(
            "Profiles were linearly interpolated at 10 dbar intervals from 10 to 700 dbar without extrapolation. TEOS-10 GSW converted Practical Salinity and in situ temperature to Absolute Salinity and Conservative Temperature. The specific-volume anomaly was integrated to dynamic height relative to 700 dbar. Successive dynamic-height differences were divided by station separation and the Coriolis parameter to obtain velocity normal to each local station segment.",
            s["body"],
        ),
        fit_image(FIGURE_VELOCITY, 172, 111),
        p(
            "Figure 1. Station path, dynamic-height profiles and section-normal relative geostrophic velocity. Positive values point left of the local A-F path. At 10 dbar the five segment velocities are +0.195, +0.131, -0.016, -0.106 and -0.492 m s<super>-1</super> for A-B through E-F. All values approach zero at the 700 dbar reference by construction.",
            s["caption"],
        ),
        PageBreak(),
        p("4. Interpretation and limits of the case", s["h1"]),
        fit_image(FIGURE_DENSITY, 172, 89),
        p(
            "Figure 2. Independent density evidence from the same six-station section. At 100 dbar the station density range is 1.804 kg m<super>-3</super>, confirming a horizontal density contrast that can support vertical geostrophic shear.",
            s["caption"],
        ),
        p("What the calculation demonstrates", s["h2"]),
        p(
            "The profiles convert the conceptual chain into an observational calculation: temperature and salinity determine density; density determines specific volume; vertical integration gives dynamic height; horizontal dynamic-height differences give relative geostrophic velocity. The sign changes among station pairs show that the cross-path shear is spatially structured rather than a single uniform current.",
            s["body"],
        ),
        p("Why the result is not an absolute current map", s["h2"]),
        p(
            "The 700 dbar velocity was set to zero, so any real reference-layer flow is omitted. The path bends, making the velocity direction different for each segment. The six profiles span about four days, so evolving fronts, tides and inertial motion can be aliased into spatial gradients. The shortest segment, E-F, gives the largest near-surface magnitude and is especially sensitive to timing and position errors. Argo spacing also cannot resolve narrow fronts or the surface Ekman layer.",
            s["body"],
        ),
        callout([
            p("Interpretation rule", s["h2"]),
            p("Treat Figure 1 as a reproducible estimate of <b>baroclinic velocity relative to 700 dbar</b>. Add an ADCP, float displacement, inverse constraint or independently justified reference velocity before calling it an absolute current.", s["body"]),
        ], background=SAND, border=CORAL),
        Spacer(1, 5 * mm),
        p("Numerical verification", s["h2"]),
        p(
            "A separate MATLAB script recomputed every exported value from Delta(dynamic height)/(f Delta s). The maximum difference was 5.55 x 10<super>-16</super> m s<super>-1</super>. It also confirmed zero dynamic height at 700 dbar and a 10 dbar range of -0.492 to +0.195 m s<super>-1</super>.",
            s["body"],
        ),
        PageBreak(),
        p("5. Submission-ready integrated answer", s["h1"]),
    ]

    full_answer = [
        "Ocean temperature is measured in situ by thermistors on CTDs, XBTs, Argo floats, gliders and moorings, and remotely by infrared or microwave satellite radiometers. In situ sensors resolve vertical structure accurately but provide limited spatial or temporal coverage, whereas satellites repeatedly map large areas but observe only the skin or near-surface ocean and require atmospheric correction and calibration. XBTs are rapid and relatively inexpensive but do not measure salinity and require fall-rate corrections.",
        "Salinity is usually derived from conductivity, temperature and pressure measured by a CTD. Bottle samples analyzed with a salinometer provide high-quality checks, and Argo extends temperature-salinity profiling over the open ocean. Satellite L-band radiometry maps surface salinity globally, but its resolution and accuracy decline near coasts, rain, ice and cold water. Conductivity sensors can drift or foul, and autonomous platforms have irregular sampling and limited recovery for recalibration.",
        "Currents are measured directly by current meters, ADCPs, surface drifters, subsurface floats and coastal HF radar. These methods provide point time series, vertical profiles, Lagrangian trajectories or surface maps. Their limitations include restricted depth or range, sparse coverage, platform motion, acoustic scatterer availability, windage, Stokes drift and coastal geometry. Satellite altimetry estimates geostrophic currents indirectly from sea-surface-height gradients and provides broad repeated coverage, but it requires orbit, geoid, tide and atmospheric corrections and cannot directly represent all small-scale or ageostrophic motions.",
        "For large-scale, slowly varying motion away from strong friction, the horizontal pressure-gradient force approximately balances the Coriolis force: f k x u_g = -(1/rho_0) grad_h p. At the sea surface, u_g = -(g/f) d eta/dy and v_g = (g/f) d eta/dx. Thus the current is parallel to sea-surface-height contours, with higher sea level on its right in the Northern Hemisphere. Horizontal temperature and salinity differences change seawater density. Under hydrostatic balance, density contrasts make the horizontal pressure gradient vary with depth, so thermal-wind balance relates horizontal density gradients to vertical geostrophic shear.",
        "Satellite altimetry can infer surface geostrophic velocity from gradients of absolute dynamic topography. CTD or Argo sections can integrate specific-volume anomaly to obtain dynamic-height differences and geostrophic velocity relative to a reference pressure. A hydrographic estimate becomes absolute only when a credible level of no motion or independent velocity is supplied. Both routes require sufficient spatial resolution, near-synoptic sampling, accurate positioning and calibration, and appropriate treatment of uncertainty.",
        "Geostrophic inference works best when the Rossby number is small, the observations are away from the equator and strong boundary friction, and hydrostatic balance is appropriate. Tides, inertial oscillations, wind-driven Ekman flow and other ageostrophic components must be small, filtered or analyzed separately. The observations must resolve the horizontal gradients rather than confuse temporal evolution with spatial structure.",
        "In the South China Sea example, six official Argo profiles sampled from 13 to 16 March 2017 were converted with TEOS-10. Dynamic-height differences relative to 700 dbar produced 10 dbar section-normal relative velocities from -0.492 to +0.195 m s^-1. This demonstrates how horizontal density structure constrains geostrophic shear, but the result remains relative because the reference-layer current is unknown. The irregular path, four-day sampling window and unresolved ageostrophic motions further limit interpretation as an instantaneous current section.",
    ]
    story += [p(paragraph, s["body"]) for paragraph in full_answer]
    story += [PageBreak(), p("6. Sources, data and reproducibility", s["h1"])]

    refs = [
        "1. NOAA Ocean Exploration. <link href='https://oceanexplorer.noaa.gov/okeanos/edu/collection/media/hdwe-WCCTD56.pdf' color='#0B6680'>What is a CTD?</link>",
        "2. NOAA Fisheries. <link href='https://www.fisheries.noaa.gov/science-blog/measuring-ocean-currents-acoustic-doppler-current-profile' color='#0B6680'>Measuring ocean currents with an Acoustic Doppler Current Profiler.</link>",
        "3. Argo Program. <link href='https://argo.ucsd.edu/data/data-from-gdacs/' color='#0B6680'>Data from Global Data Assembly Centres.</link>",
        "4. Argo data citation: Argo (2000). Argo float data and metadata from Global Data Assembly Centre. <link href='https://doi.org/10.17882/42182' color='#0B6680'>doi:10.17882/42182</link>.",
        "5. TEOS-10. <link href='https://www.teos-10.org/software.htm' color='#0B6680'>Gibbs SeaWater software</link> and <link href='https://www.teos-10.org/pubs/gsw/html/gsw_geostrophic_velocity.html' color='#0B6680'>geostrophic-velocity documentation</link>.",
        "6. U.S. IOOS. <link href='https://ioos.noaa.gov/project/hf-radar/' color='#0B6680'>High-frequency radar surface-current observing network.</link>",
        "7. NOAA OISST v2.1. <link href='https://doi.org/10.25921/RE9P-PT57' color='#0B6680'>Daily 0.25 degree sea-surface-temperature analysis.</link>",
        "8. NASA JPL PO.DAAC. <link href='https://podaac.jpl.nasa.gov/dataset/NEUROST_SSH-SST_L4_V2024.0' color='#0B6680'>Sea-surface height and geostrophic-current variables.</link>",
    ]
    story += [p(ref, s["reference"]) for ref in refs]
    story += [
        Spacer(1, 4 * mm),
        p("Case-data record", s["h2"]),
        p(
            "The six NetCDF files were downloaded from https://data-argo.ifremer.fr/dac/ on 20 October 2026. The submitted data package contains the raw profiles, processed dynamic-height and velocity CSV files, the JSON method and hash manifest, the Python analysis script, the MATLAB validation script and a README. Station separations are 281.3, 79.5, 204.6, 84.4 and 38.2 km.",
            s["body"],
        ),
        p("Reproducibility checks", s["h2"]),
        p("• 6 stations x 70 pressure levels = 420 processed profile rows.<br/>• 5 station pairs x 70 pressure levels = 350 velocity rows.<br/>• Dynamic height and relative velocity equal zero at the 700 dbar reference.<br/>• Exported velocities agree with the independent MATLAB calculation to 5.55 x 10<super>-16</super> m s<super>-1</super>.", s["body"]),
        Spacer(1, 6 * mm),
        callout([
            p("Scope statement", s["h2"]),
            p("The observational calculation supports the physical explanation and provides a realistic magnitude check. It does not establish an absolute current because no independent reference velocity was available.", s["body"]),
        ], background=MINT, border=TEAL),
    ]

    doc.build(story)
    print(f"Wrote {OUTPUT}")
    print(f"Case range: {section['near_surface_range_m_s']}")


if __name__ == "__main__":
    build()
