import pandas as pd
import ast
import re
from groq import Groq
import concurrent.futures
import os
import itertools

os.environ["GROQ_API_KEY"] = "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"

def string_to_list(x):
    try:
        if isinstance(x, str):
            return ast.literal_eval(x)
        return x
    except Exception:
        return x

def get_groq():
    return Groq()

# List of subtopics
d = {
    "physical data and processes": [
        "acceleration of particles",
        "accretion, accretion disks",
        "asteroseismology",
        "astrobiology",
        "astrochemistry",
        "astroparticle physics",
        "atomic data",
        "atomic processes",
        "black hole physics",
        "chaos",
        "conduction",
        "convection",
        "dense matter",
        "diffusion",
        "dynamo",
        "elementary particles",
        "equation of state",
        "gravitation",
        "gravitational lensing: strong",
        "gravitational lensing: weak",
        "gravitational lensing: micro",
        "gravitational waves",
        "hydrodynamics",
        "instabilities",
        "line: formation",
        "line: identification",
        "line: profiles",
        "magnetic fields",
        "magnetic reconnection",
        "magnetohydrodynamics (MHD)",
        "masers",
        "molecular data",
        "molecular processes",
        "neutrinos",
        "nuclear reactions, nucleosynthesis, abundances",
        "opacity",
        "plasmas",
        "polarization",
        "radiation: dynamics",
        "radiation mechanisms: general",
        "radiation mechanisms: non-thermal",
        "radiation mechanisms: thermal",
        "radiative transfer",
        "relativistic processes",
        "scattering",
        "shock waves",
        "solid state: refractory",
        "solid state: volatile",
        "turbulence",
        "waves"
    ],
    "astronomical instrumentation methods and techniques": [
        "atmospheric effects",
        "balloons",
        "instrumentation: adaptive optics",
        "instrumentation: detectors",
        "instrumentation: high angular resolution",
        "instrumentation: interferometers",
        "instrumentation: miscellaneous",
        "instrumentation: photometers",
        "instrumentation: polarimeters",
        "instrumentation: spectrographs",
        "light pollution",
        "methods: analytical",
        "methods: data analysis",
        "methods: laboratory: atomic",
        "methods: laboratory: molecular",
        "methods: laboratory: solid state",
        "methods: miscellaneous",
        "methods: numerical",
        "methods: observational",
        "methods: statistical",
        "site testing",
        "space vehicles",
        "space vehicles: instruments",
        "techniques: high angular resolution",
        "techniques: image processing",
        "techniques: imaging spectroscopy",
        "techniques: interferometric",
        "techniques: miscellaneous",
        "techniques: photometric",
        "techniques: polarimetric",
        "techniques: radar astronomy",
        "techniques: radial velocities",
        "techniques: spectroscopic",
        "telescopes"
    ],
    "astronomical databases": [
        "astronomical databases: miscellaneous",
        "atlases",
        "catalogs",
        "surveys",
        "virtual observatory tools"
    ],
    "astrometry and celestial mechanics": [
        "astrometry",
        "celestial mechanics",
        "eclipses",
        "ephemerides",
        "occultations",
        "parallaxes",
        "proper motions",
        "reference systems",
        "time"
    ],
    "the sun": [
        "Sun: abundances",
        "Sun: activity",
        "Sun: atmosphere",
        "Sun: chromosphere",
        "Sun: corona",
        "Sun: coronal mass ejections (CMEs)",
        "Sun: evolution",
        "Sun: faculae, plages",
        "Sun: filaments, prominences",
        "Sun: flares",
        "Sun: fundamental parameters",
        "Sun: general",
        "Sun: granulation",
        "Sun: helioseismology",
        "Sun: heliosphere",
        "Sun: infrared",
        "Sun: interior",
        "Sun: magnetic fields",
        "Sun: oscillations",
        "Sun: particle emission",
        "Sun: photosphere",
        "Sun: radio radiation",
        "Sun: rotation",
        "solar–terrestrial relations",
        "solar wind",
        "sunspots",
        "Sun: transition region",
        "Sun: UV radiation",
        "Sun: X-rays, gamma rays"
    ],
    "planetary systems": [
        "comets: general",
        "comets: individual (…, …)",
        "Earth",
        "interplanetary medium",
        "Kuiper belt: general",
        "Kuiper belt objects: individual (…, …)",
        "meteorites, meteors, meteoroids",
        "minor planets, asteroids: general",
        "minor planets, asteroids: individual (…, …)",
        "Moon",
        "Oort Cloud",
        "planets and satellites: atmospheres",
        "planets and satellites: aurorae",
        "planets and satellites: composition",
        "planets and satellites: detection",
        "planets and satellites: dynamical evolution and stability",
        "planets and satellites: formation",
        "planets and satellites: fundamental parameters",
        "planets and satellites: gaseous planets",
        "planets and satellites: general",
        "planets and satellites: individual (…, …)",
        "planets and satellites: interiors",
        "planets and satellites: magnetic fields",
        "planets and satellites: oceans",
        "planets and satellites: physical evolution",
        "planets and satellites: rings",
        "planets and satellites: surfaces",
        "planets and satellites: tectonics",
        "planets and satellites: terrestrial planets",
        "protoplanetary disks",
        "planet–disk interactions",
        "planet–star interactions",
        "zodiacal dust"
    ],
    "stars": [
        "stars: abundances",
        "stars: activity",
        "stars: AGB and post-AGB",
        "stars: atmospheres",
        "stars: binaries (including multiple): close",
        "stars: binaries: eclipsing",
        "stars: binaries: general",
        "stars: binaries: spectroscopic",
        "stars: binaries: symbiotic",
        "stars: binaries: visual",
        "stars: black holes",
        "stars: blue stragglers",
        "stars: brown dwarfs",
        "stars: carbon",
        "stars: chemically peculiar",
        "stars: chromospheres",
        "stars: circumstellar matter",
        "stars: coronae",
        "stars: distances",
        "stars: dwarf novae",
        "stars: early-type",
        "stars: emission-line, Be",
        "stars: evolution",
        "stars: flare",
        "stars: formation",
        "stars: fundamental parameters",
        "stars: general",
        "stars: gamma ray burst: general",
        "stars: gamma ray burst: individual (…, …)",
        "stars: Hertzsprung–Russell and C–M diagrams",
        "stars: horizontal-branch",
        "stars: imaging",
        "stars: individual (…, …)",
        "stars: interiors",
        "stars: jets",
        "stars: kinematics and dynamics",
        "stars: late-type",
        "stars: low-mass",
        "stars: luminosity function, mass function",
        "stars: magnetars",
        "stars: magnetic field",
        "stars: massive",
        "stars: mass-loss",
        "stars: neutron",
        "stars: novae, cataclysmic variables",
        "stars: oscillations (including pulsations)",
        "stars: peculiar (except chemically peculiar)",
        "stars: planetary systems",
        "stars: Population II",
        "stars: Population III",
        "stars: pre-main sequence",
        "stars: protostars",
        "stars: pulsars: general",
        "stars: pulsars: individual (…, …)",
        "stars: rotation",
        "stars: solar-type",
        "stars: starspots",
        "stars: statistics",
        "stars: subdwarfs",
        "stars: supergiants",
        "stars: supernovae: general",
        "stars: supernovae: individual (…, …)",
        "stars: variables: Cepheids",
        "stars: variables: delta Scuti",
        "stars: variables: general",
        "stars: variables: RR Lyrae",
        "stars: variables: S Doradus",
        "stars: variables: T Tauri, Herbig Ae/Be",
        "stars: white dwarfs",
        "stars: winds, outflows",
        "stars: Wolf–Rayet"
    ],
    "interstellar medium (ism) nebulae": [
        "ISM: abundances",
        "ISM: atoms",
        "ISM: bubbles",
        "ISM: clouds",
        "ISM: cosmic rays",
        "ISM: dust, extinction",
        "ISM: evolution",
        "ISM: general",
        "ISM: HII regions",
        "ISM: Herbig–Haro objects",
        "ISM: individual objects (…, …) (except planetary nebulae)",
        "ISM: jets and outflows",
        "ISM: kinematics and dynamics",
        "ISM: lines and bands",
        "ISM: magnetic fields",
        "ISM: molecules",
        "ISM: planetary nebulae: general",
        "ISM: planetary nebulae: individual (…, …)",
        "ISM: photon-dominated region (PDR)",
        "ISM: structure",
        "ISM: supernova remnants"
    ],
    "the galaxy": [
        "Galaxy: abundances",
        "Galaxy: bulge",
        "Galaxy: center",
        "Galaxy: disk",
        "Galaxy: evolution",
        "Galaxy: formation",
        "Galaxy: fundamental parameters",
        "Galaxy: general",
        "Galaxy: globular clusters: general",
        "Galaxy: globular clusters: individual (…, …)",
        "Galaxy: halo",
        "Galaxy: local interstellar matter",
        "Galaxy: kinematics and dynamics",
        "Galaxy: nucleus",
        "Galaxy: open clusters and associations: general",
        "Galaxy: open clusters and associations: individual (…, …)",
        "Galaxy: solar neighborhood",
        "Galaxy: stellar content",
        "Galaxy: structure"
    ],
    "galaxies": [
        "galaxies: abundances",
        "galaxies: active",
        "galaxies: BL Lacertae objects: general",
        "galaxies: BL Lacertae objects: individual (…, …)",
        "galaxies: bulges",
        "galaxies: clusters: general",
        "galaxies: clusters: individual (…, …)",
        "galaxies: clusters: intracluster medium",
        "galaxies: distances and redshifts",
        "galaxies: dwarf",
        "galaxies: elliptical and lenticular, cD",
        "galaxies: evolution",
        "galaxies: formation",
        "galaxies: fundamental parameters",
        "galaxies: general",
        "galaxies: groups: general",
        "galaxies: groups: individual (…, …)",
        "galaxies: halos",
        "galaxies: high-redshift",
        "galaxies: individual (…, …)",
        "galaxies: interactions",
        "galaxies: intergalactic medium",
        "galaxies: irregular",
        "galaxies: ISM",
        "galaxies: jets",
        "galaxies: kinematics and dynamics",
        "galaxies: Local Group",
        "galaxies: luminosity function, mass function",
        "galaxies: Magellanic Clouds",
        "galaxies: magnetic fields",
        "galaxies: nuclei",
        "galaxies: peculiar",
        "galaxies: photometry",
        "galaxies: quasars: absorption lines",
        "galaxies: quasars: emission lines",
        "galaxies: quasars: general",
        "galaxies: quasars: individual (…, …)",
        "galaxies: quasars: supermassive black holes",
        "galaxies: Seyfert",
        "galaxies: spiral",
        "galaxies: starburst",
        "galaxies: star clusters: general",
        "galaxies: star clusters: individual (…, …)",
        "galaxies: star formation",
        "galaxies: statistics",
        "galaxies: stellar content",
        "galaxies: structure"
    ],
    "cosmology": [
        "cosmology: cosmic background radiation",
        "cosmology: cosmological parameters",
        "cosmology: miscellaneous",
        "cosmology: observations",
        "cosmology: theory",
        "cosmology: dark ages, reionization, first stars",
        "cosmology: dark matter",
        "cosmology: dark energy",
        "cosmology: diffuse radiation",
        "cosmology: distance scale",
        "cosmology: early universe",
        "cosmology: inflation",
        "cosmology: large-scale structure of universe",
        "cosmology: primordial nucleosynthesis"
    ],
    "resolved and unresolved sources as a function of wavelength": [
        "gamma rays: diffuse background",
        "gamma rays: galaxies",
        "gamma rays: galaxies: clusters",
        "gamma rays: general",
        "gamma rays: ISM",
        "gamma rays: stars",
        "infrared: diffuse background",
        "infrared: galaxies",
        "infrared: general",
        "infrared: ISM",
        "infrared: planetary systems",
        "infrared: stars",
        "radio continuum: galaxies",
        "radio continuum: general",
        "radio continuum: ISM",
        "radio continuum: planetary systems",
        "radio continuum: stars",
        "radio lines: galaxies",
        "radio lines: general",
        "radio lines: ISM",
        "radio lines: planetary systems",
        "radio lines: stars",
        "submillimeter: diffuse background",
        "submillimeter: galaxies",
        "submillimeter: general",
        "submillimeter: ISM",
        "submillimeter: planetary systems",
        "submillimeter: stars",
        "ultraviolet: galaxies",
        "ultraviolet: general",
        "ultraviolet: ISM",
        "ultraviolet: planetary systems",
        "ultraviolet: stars",
        "X-rays: binaries",
        "X-rays: bursts",
        "X-rays: diffuse background",
        "X-rays: galaxies",
        "X-rays: galaxies: clusters",
        "X-rays: general",
        "X-rays: individual (…, …)",
        "X-rays: ISM",
        "X-rays: stars"
    ]
}

def process_row(idx, row, groq_client, prompt_template, dict_str, top_words_col, top_bigrams_col, top_trigrams_col):
    top_words = string_to_list(row.get(top_words_col, []))
    top_bigrams = string_to_list(row.get(top_bigrams_col, []))
    top_trigrams = string_to_list(row.get(top_trigrams_col, []))
    
    top_words_str = str(top_words)
    top_bigrams_str = str(top_bigrams)
    top_trigrams_str = str(top_trigrams)
    
    prompt = prompt_template.format(
        dictionary=dict_str,
        top_words=top_words_str,
        top_bigrams=top_bigrams_str,
        top_trigrams=top_trigrams_str
    )
    
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300,
            top_p=1,
            stream=False
        )
        if hasattr(response.choices[0].message, 'content'):
            response_text = response.choices[0].message.content.strip()
        else:
            response_text = "".join(chunk.choices[0].delta.content for chunk in response).strip()
        
        print(f"Raw response for row {idx}: {response_text}")
        
        if response_text.startswith("[") and response_text.endswith("]"):
            list_str = response_text
        else:
            match = re.search(r'\[.*\]', response_text, re.DOTALL)
            list_str = match.group(0) if match else "[]"
        
        try:
            subtopics_list = ast.literal_eval(list_str)
            if not isinstance(subtopics_list, list):
                subtopics_list = []
        except Exception as parse_err:
            print(f"Parsing error for row {idx}: {parse_err}")
            subtopics_list = []
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        subtopics_list = []
    return idx, subtopics_list

def generate_expertise(df, groq_client=None,
                       top_words_col="Top 10 Words",
                       top_bigrams_col="Top 10 Bigrams",
                       top_trigrams_col="Top 10 Trigrams",
                       subtopics_dict=None, max_workers=2):
    if groq_client is None:
        groq_client = get_groq()
    if subtopics_dict is None:
        subtopics_dict = d 
    
    dict_str = ""
    for parent, sub_list in subtopics_dict.items():
        dict_str += parent + ":\n" + ", ".join(sub_list).strip() + "\n\n"
    
    prompt_template = """
You are a highly knowledgeable astrophysicist. You are provided with three ordered lists of n-grams (top words, bigrams, and trigrams) extracted from a researcher's ADS abstracts. Although the top words list is longer, do not assume that higher frequency implies greater importance over the bigrams or trigrams. Consider all three lists together to determine the researcher's core expertise, responding with that and that only, and no other text.

Your task:
1. Analyze these n-grams holistically.
2. Select 1 to 3 subtopics that best capture the researcher's true areas of expertise.
3. Use ONLY the provided dictionary below as your source; do not invent any new categories.
4. If a chosen subtopic has additional specificity (i.e. a nested subtopic), format it as "parent:subtopic:sub-subtopic". Otherwise, use "parent:subtopic".
5. Return ONLY a Python list of strings (for example, ["stars:stellar evolution", "cosmology:dark energy"]) with no additional commentary or text. This is a must do, no exceptions.

Dictionary of Allowed Topics and Subtopics:
{dictionary}

Researcher's n-grams (with occurrence counts):
Top 10 Trigrams: {top_trigrams}
Top 10 Bigrams: {top_bigrams}
Top 10 Words: {top_words}
"""
    results = {}
    total_rows = len(df)
    print(f"Extracting subtopics for {total_rows} rows in parallel with max_workers={max_workers}...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(process_row, idx, row, groq_client, prompt_template, dict_str,
                             top_words_col, top_bigrams_col, top_trigrams_col): idx
            for idx, row in df.iterrows()
        }
        for future in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                idx_returned, subtopics_list = future.result()
                results[idx_returned] = subtopics_list
            except Exception as exc:
                results[idx] = []
                print(f"Row {idx} generated an exception: {exc}")
    
    subtopics_column = [results[i] for i in range(len(df))]
    df["Subtopics"] = subtopics_column
    return df
