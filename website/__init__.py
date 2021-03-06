import collections
import pandas as pd


CUSTOM_CATEGORIES_INDEX = pd.MultiIndex.from_tuples(
    [
        ("examination", "Audiometry"),
        ("examination", "Blood__Pressure"),
        ("examination", "Body__Measures"),
        ("examination", "Dual__Energy__X-ray__Absorptiometry__-__Android_or_Gynoid"),
        ("examination", "Dual__Energy__X-ray__Absorptiometry__-__Femur"),
        ("examination", "Lower__Extremity__Disease__-__Ankle__Brachial__Blood__Pressure__Index"),
        ("examination", "Muscle__Strength__-__Grip__Test"),
        ("examination", "Oral__Health"),
        ("examination", "Oral__Health__-__Addendum"),
        ("examination", "Oral__Health__-__Dentition"),
        ("examination", "Spirometry__-__Pre__and__Post-Bronchodilator"),
        ("examination", "Vision"),
        ("laboratory", "Cadmium,__Lead,__Mercury,__Cotinine__&__Nutritional__Biochemistries"),
        ("laboratory", "Complete__Blood__Count__with__5-part__Differential__-__Whole__Blood"),
        ("laboratory", "Cystatin__C__(Surplus)"),
        ("laboratory", "Fatty__Acids__-__Serum"),
        ("laboratory", "Glycohemoglobin"),
        ("laboratory", "Non-dioxin-like__Polychlorinated__Biphenyls"),
        ("laboratory", "Plasma__Fasting__Glucose,__Serum__C-peptide__&__Insulin"),
        ("laboratory", "Standard__Biochemistry__Profile"),
        ("laboratory", "Trans__Fatty__Acids"),
        ("laboratory", "Vitamin__A,__Vitamin__E__&__Carotenoids"),
        ("questionnaire", "Blood__Pressure__&__Cholesterol"),
        ("questionnaire", "Current__Health__Status"),
        ("questionnaire", "Hospital__Utilization__&__Access__to__Care"),
        ("questionnaire", "Housing__Characteristics"),
        ("questionnaire", "Immunization"),
        ("questionnaire", "Physical__Functioning"),
        ("questionnaire", "Smoking__-__Recent__Tobacco__Use"),
        ("questionnaire", "Vision"),
    ],
    names=["main_category", "category"],
)


def create_dictionaries(main_category, list_categories):
    dict_categories = dict(
        zip(
            list_categories,
            list(map(lambda cat: cat.replace("_or_", "/").replace("__", " ").replace("--", "."), list_categories)),
        )
    )
    sorted_dict_categories = {"all": "All"}
    sorted_dict_categories.update(sorted(dict_categories.items()))
    main_category_categories = collections.OrderedDict(sorted_dict_categories)

    list_custom_categories = (
        CUSTOM_CATEGORIES_INDEX[CUSTOM_CATEGORIES_INDEX.get_level_values("main_category") == main_category]
        .get_level_values("category")
        .to_list()
    )
    dict_custom_categories = dict(
        zip(
            list_custom_categories,
            list(
                map(
                    lambda cat: cat.replace("_or_", "/").replace("__", " ").replace("--", "."),
                    list_custom_categories,
                )
            ),
        )
    )
    sorted_dict_custom_categories = {"all": "All"}
    sorted_dict_custom_categories.update(sorted(dict_custom_categories.items()))
    main_category_custom_categories = collections.OrderedDict(sorted_dict_custom_categories)

    return main_category_categories, main_category_custom_categories


METHODS = {"pearson": "Pearson", "spearman": "Spearman"}

TARGETS = {"age": "Age", "all": "Survival all", "cvd": "Survival CVD", "cancer": "Survival cancer"}

MAIN_CATEGORIES = {"examination": "Examination", "laboratory": "Laboratory", "questionnaire": "Questionnaire"}

LIST_EXAMINATION_CATEGORIES = [
    "Dual-Energy__X-ray__Absorptiometry__-__FRAX__Score",
    "Exhaled__Nitric__Oxide",
    "Dual__Energy__X-ray__Absorptiometry__-__Android_or_Gynoid",
    "Taste__&__Smell",
    "Ophthalmology__-__Retinal__Imaging",
    "Oral__Health__-__Recommendation__of__Care",
    "Dermatology",
    "Bioelectrical__Impedance__Analysis",
    "Body__Measures",
    "Lower__Extremity__Disease__-__Peripheral__Neuropathy",
    "Blood__Pressure__-__Oscillometric__Measurements",
    "Muscle__Strength__-__Grip__Test",
    "Dual__Energy__X-ray__Absorptiometry__-__Femur",
    "Dual-Energy__X-ray__Absorptiometry__-__Whole__Body,__Second__Exam",
    "Audiometry__-__Tympanometry",
    "Arthritis__Body__Measures",
    "Vision",
    "Cardiovascular__Fitness",
    "Oral__Health__-__Dentition",
    "Dual-Energy__X-ray__Absorptiometry__-__T4__Vertebrae__Morphology",
    "Blood__Pressure",
    "Dual-Energy__X-ray__Absorptiometry__-__Whole__Body",
    "Shared__Exclusion__Questions",
    "Balance",
    "Muscle__Strength",
    "Oral__Health__-__Periodontal_or_Lower",
    "Oral__Health__-__Periodontal_or_Upper",
    "Audiometry__-__Acoustic__Reflex",
    "Spirometry__-__Pre__and__Post-Bronchodilator",
    "Liver__Ultrasound__Transient__Elastography",
    "Physical__Activity__Monitor__-__Header",
    "Oral__Health",
    "Lower__Extremity__Disease__-__Ankle__Brachial__Blood__Pressure__Index",
    "Dual__Energy__X-ray__Absorptiometry__-__Spine",
    "Fluorosis__-__Clinical",
    "Oral__Health__-__Periodontal",
    "Ophthalmology__-__Frequency__Doubling__Technology",
    "Oral__Health__-__Addendum",
    "Dual-Energy__X-ray__Absorptiometry__-__Vertebral__Fracture__Assessment",
    "Audiometry",
    "Dual-Energy__X-ray__Absorptiometry__-__Abdominal__Aortic__Calcification",
    "Tuberculosis",
]
EXAMINATION_CATEGORIES, EXAMINATION_CUSTOM_CATEGORIES = create_dictionaries("examination", LIST_EXAMINATION_CATEGORIES)


LIST_LABORATORY_CATEGORIES = [
    "Lead__-__Dust",
    "Pesticides__-__Current__Use__-__Urine__(Formerly__Priority__Pesticides,__Non-persistent__Pesticide__Metabolites)",
    "Hepatitis__E__:__IgG__&__IgM__Antibodies",
    "Non-dioxin-like__Polychlorinated__Biphenyls",
    "Cholesterol__-__Total",
    "Flame__Retardant__Metabolites__-__Urine__(Surplus)",
    "Fatty__Acids__-__Serum",
    "Personal__Care__and__Consumer__Product__Chemicals__and__Metabolites",
    "Autoantibodies__-__Immunofluorescence__&__Immunoprecipitation__Analyses__(Surplus)",
    "Human__Papillomavirus__(HPV)__-__6,__11,__16__&__18__Antibody__-__Serum:__4-plex__CLIA",
    "Standard__Biochemistry__Profile__&__Hormones",
    "Albumin__&__Creatinine__-__Urine",
    "Vitamin__C",
    "Cadmium,__Lead,__&__Total__Mercury__-__Blood",
    "Hepatitis__B__Surface__Antibody",
    "Cytomegalovirus__IgG__&__IgM__Antibodies__-__Serum",
    "Methicillin__-__Resistant__Staphylococcus__aureus__(MRSA)",
    "Human__Papillomavirus__(HPV)__-__6,__11,__16__&__18__Antibody__???__Serum:__4-plex__CLIA",
    "Volatile__Organic__Compounds__&__Metabolites__-__Urine",
    "Standard__Biochemistry__Profile",
    "Volatile__Organic__Compounds__and__Trihalomethanes_or_MTBE__-__Blood",
    "Mercury__-__Hair",
    "Varicella-Zoster__Virus__Antibody__(Surplus)",
    "Volatile__Organic__Compounds__(VOC)__-__Personal__Exposure__Badge",
    "Polyfluoroalkyl__Chemicals",
    "Melamine__-__Urine__(Surplus)",
    "C-Reactive__protein__(CRP),__Fibrinogen,__Bone__Alkaline__Phosphatase__&__Urinary__N-telopeptides",
    "Ferritin__&__Transferrin__Receptor",
    "Volatile__Organic__Compounds__-__Blood__&__Water",
    "Glycohemoglobin,__Plasma__Glucose,__Serum__C-peptide,__&__Insulin,__Second__Exam",
    "Volatile__Organic__Compounds__-__Blood,__Water,__&__Related__Questionnaire__Items",
    "Aflatoxin__B1-lysine__-__Serum__(Surplus)",
    "Fluoride__-__Plasma",
    "Vitamin__B12",
    "Epstein-Barr__Virus__(VCA__IgG)__-__Serum__(Surplus)",
    "Ethylene__Oxide",
    "Toxoplasma__(IgG),__Toxoplasma__(IgM),Toxoplasma__(Dye),Toxoplasma__Differential__Agglutination,__&__Toxoplasma__(Avidity)",
    "Complete__Blood__Count__with__5-part__Differential__-__Whole__Blood",
    "Perfluoroaokyl__Chemicals__-__Serum__(Surplus)",
    "Sex__Steroid__Hormone__-__Men__(Surplus)",
    "Hepatitis__C:__Confirmed__Antibody__(INNO-LIA)__-__2015",
    "Phthalates__and__Plasticizers__Metabolites__-__Urine",
    "Cadmium,__Lead,__Total__Mercury,__Selenium,__&__Manganese__-__Blood",
    "Cotinine,__Hydroxycotinine,__&__Other__Nicotine__Metabolites__and__Analogs__-__Urine",
    "Cadmium,__Lead,__Total__Mercury,__Ferritin,__Serum__Folate,__RBC__Folate,__Vitamin__B12,__Homocysteine,__Methylmalonic__acid,__Cotinine__-__Blood,__Second__Exam",
    "Caffeine__&__Caffeine__Metabolites__-__Urine",
    "Fluoride__-__Water",
    "Environmental__Phenols",
    "DEET__Metabolites__-__Urine__-__Surplus",
    "Hepatitis__A__Antibody",
    "Plasma__Fasting__Glucose__&__Insulin",
    "Flame__Retardants__-__Urine____(Surplus)",
    "Organophosphate__Insecticides__-__Diakyl__Phosphate__Metabolites__-__Urine",
    "Chlamydia__Pgp3__(plasmid__gene__product__3)__ELISA__(enzyme__linked__immunosorbent__assay)__and__multiplex__bead__array__(MBA)__results",
    "Pyrethroids,__Herbicides,__&__OP__Metabolites__-__Urine",
    "Perfluoroalkyl__and__Polyfluoroalkyl__Substances__in__US__children__3-11__Years__of__Age",
    "Urine__Specific__Gravity__Measurement__(Surplus)",
    "High-Sensitivity__C-Reactive__Protein__(hs-CRP)",
    "Measles,__Rubella,__&__Varicella",
    "Poliovirus__Serotypes__1,__2,__&__3__Antibodies__-__Serum__(Surplus)",
    "Polyaromatic__Hydrocarbons__(PAHs)__-__Urine",
    "Polychlorinated__dibenzo-p-dioxins__(PCDDs),__Dibenzofurans__(PCDFs)__&__Coplanar__Polychlorinated__Biphenyls__(cPCBs)____-__Pooled__Samples",
    "Perchlorate,__Nitrate__&__Iodide__-__Tap__Water",
    "Human__Papillomavirus__(HPV)__-__Multiplexed__6,__11,__16,__18,__31,__22,__45,__52__&__58__Antibody__???__Serum:__9-plex__CLIA",
    "Syphilis-IgG,__Syphilis__Rapid__Plasma__Reagin__(RPR)__&__Treponema__pallidum__Particle__Agglutination__(TP-PA)",
    "Mercury__-__Inorganic,__Ethyl__&__Methyl__-__Blood",
    "Monoclonal__gammopathy__of__undetermined__significance__(MGUS)__(Surplus)",
    "Methylmalonic__Acid",
    "Herpes__Simplex__Virus__Type-2__-__Youth",
    "Hepatitis__B:__Core__Antibody,__Surface__Antigen;__Hepatitis__D__Antibody",
    "Sex__Steroid__Hormone__-__Serum",
    "Chlamydia__&__Gonorrhea__-__Urine__-__Youth",
    "Volatile__Organic__Compounds__-__Water__&__Related__Questionnaire__Items",
    "Cholesterol__-__LDL__&__Triglycerides",
    "Folate__Forms__-__Total__&__Individual__-__Serum",
    "Human__Papillomavirus__(HPV)__DNA__-__Vaginal__Swab:__Digene__Hybrid__Capture__&__Prototype__Line__Blot__Assay",
    "Acrylamide__&__Glycidamide",
    "Anti-Mullerian__Hormone__(AMH)__&__Inhibin-B__(Surplus)",
    "Folic__Acid__-__Unmetabolized__(Surplus)",
    "Tobacco-specific__Nitrosamines__(TSNAs)__-__Urine",
    "Vitamin__A,__Vitamin__E,__&__Carotenoids,__Second__Exam",
    "Cotinine__-__Serum__&__Total__NNAL__-__Urine",
    "Volatile__Organic__Compound__(VOC)__Metabolites__-__Urine",
    "Cystatin__C__(Surplus)",
    "Mercury__-__Inorganic__-__Blood",
    "Human__Papillomavirus__(HPV)__DNA__-__Vaginal__Swab:__Roche__Cobas__&__Roche__Linear__Array",
    "Mono-2-ethyl-5-hydroxyhexyl__terephthalate,__mono-2-ethyl-5-carboxypentyl__terephthalate,__and__monooxoisononyl__phthalate__-__Urine__(Surplus)",
    "Imidacloprid,__5-Hydroxy__imidacloprid,__Acetamiprid,__N-desmethyl__Acetamiprid,__Clothianidin,__and__Thiacloprid__in__NHANES__2015-16__Surplus__Urine",
    "Plasma__Fasting__Glucose,__Serum__C-peptide__&__Insulin",
    "Cadmium,__Lead,__Mercury,__Cotinine__&__Nutritional__Biochemistries",
    "Perfluoroalkyl__and__Polyfluoroalkyl",
    "Iron__Status__-__Serum",
    "Phthalates__-__Urine",
    "Chromium__&__Cobalt",
    "Thyroid__Profile",
    "Cotinine,__Hydroxycotinine,__&__Other__Nicotine__Metabolites__and__Analogs__-__Urine__-__Special__Sample",
    "Aromatic__Diamines__-__Urine",
    "Norovirus__antibody__-__Serum",
    "Vitamin__D",
    "Aldehydes__-__Serum__-__Special__Sample",
    "Phthalates__&__Plasticizers__Metabolites__-__Urine",
    "Polycyclic__Aromatic__Hydrocarbons__(PAH)__-__Urine",
    "Mercury__-__Inorganic,__Urine",
    "Human__Papillomavirus__(HPV)__-__Oral__Rinse",
    "Pesticides__-__Environmental__-__Urine",
    "Heterocyclic__Aromatic__Amines__-__Urine",
    "Perchlorate,__Nitrate__&__Thiocyanate__-__Urine",
    "Transferrin__Receptor__-__Pregnant__Women__(Surplus)",
    "Mercury:__Inorganic,__Ethyl__and__Methyl__-__Blood",
    "Phytoestrogens__-__Urine",
    "Perfluoroalkyl__and__Polyfluoroalkyl__Substances",
    "Mumps__Antibody__-__Serum__(Surplus)",
    "Volatile__N-Nitrosamine__Compounds__(VNAs)__-__Urine",
    "Perfluoroalkyl__and__Polyfluoroalkyl__Substances__-__Linear__and__Branched__PFOS__and__PFOA__Isomers__(Surplus)",
    "Thyroid__Profile__(Surplus)",
    "Total__Testosterone",
    "Phthalates,__Phytoestrogens__&__PAHs__-__Urine__PHPYPA__Urinary__Phthalates",
    "Folate__-__RBC",
    "Toxoplasma__gondii__Antibody__-__Serum__(Surplus)",
    "Toxoplasma__Gondii__Antibody__-__Serum__(Surplus)",
    "Phthalates__and__Plasticizers__Metabolites__-__Urine__(Surplus)",
    "Perchlorate,__Nitrate__&__Thiocyanate__-__Urine__(Surplus)",
    "Trans__Fatty__Acids",
    "Oral__Glucose__Tolerance__Test",
    "C-Reactive__Protein__(CRP)",
    "Tissue__Transglutaminase__Assay__(IgA-TTG)__&__IgA__Endomyseal__Antibody__Assay__(IgA__EMA)",
    "Brominated__Flame__Retardants__(BFRs)",
    "Insulin",
    "Cytomegalovirus__Antibodies__-__Serum__(Surplus)",
    "Cancer__antigen__CA125__and__CA15--3__-__Serum",
    "Measles,__Rubella,__&__Varicella,__Second__Exam",
    "Iron,__Total__Iron__Binding__Capacity__(TIBC),__&__Transferrin__Saturation",
    "Volatile__Organic__Compounds__-__Trihalomethanes_or_MTBE_or_Nitromethane__-__Blood",
    "Nickel__-__Urine",
    "Iodine__-__Urine",
    "Folate__Forms__-__Individual__-__Serum",
    "Urine__Flow__Rate",
    "Herpes__Simplex__Virus__Type-1__(Surplus)",
    "Cadmium,__Lead,__Ferritin,__Serum__Folate,__RBC__Folate,__Vitamin__B12,__Homocysteine,__Methylmalonic__acid,__Cotinine__&__Other__Selected__Nutritional__Biochemistries__-__Blood,__Second__Exam",
    "Volatile__Organic__Compounds__(VOCs)__-__Blood",
    "Aldehydes__-__Serum",
    "Metals__-__Urine",
    "Prostate__Specific__Antigen__(PSA)",
    "Fasting__Questionnaire",
    "Arsenics__-__Total__&__Speciated__-__Urine",
    "HIV__Antibody__Test",
    "Pooled-Sample__Technical__Support__File",
    "Herpes__Simplex__Virus__Type-1__&__Type-2",
    "Cotinine__and__Hydroxycotinine__-__Serum",
    "Standard__Biochemistry__Profile__&__Hormones,__Second__Exam",
    "Fatty__Acids__-__Plasma__(Surplus)",
    "Pregnancy__Test__-__Urine",
    "Transferrin__Receptor",
    "Chromium__-__Urine",
    "Parathyroid__Hormone",
    "Thyroid__-__Stimulating__Hormone__&__Thyroxine__(TSH__&__T4)",
    "DEET__and__Metabolites",
    "HIV__Antibody__Test,__CD4+__T__Lymphocytes__&__CD8+__T__Cells",
    "Allergens__-__Household__Dust",
    "Vitamin__B6",
    "Prostate-specific__Antigen__(PSA),__Second__Exam",
    "Vitamin__A,__Vitamin__E__&__Carotenoids",
    "Autoantibodies__-__Immunofluorescence__Analyses__(Surplus)",
    "Volatile__Organic__Compounds__(VOCs)__and__Trihalomethanes_or_MTBE__-__Blood__-__Special__Sample",
    "Antibody__to__Toxocara__spp--__(Surplus)",
    "Osmolality__-__Urine",
    "Cholesterol__-__Low-Density__Lipoproteins__(LDL)__&__Triglycerides",
    "Measles,__Mumps,__Rubella__&__Varicella",
    "Atrazine__and__Metabolites",
    "Latex",
    "Creatinine__&__Albumin__-__Urine,__Second__Exam",
    "Cholesterol__-__HDL",
    "Hepatitis__C__RNA__(HCV-RNA)__&__HCV__Genotype__(Surplus)",
    "Complete__Blood__Count__with__5-Part__Differential",
    "Tuberculosis__-__Quantiferon_In_Gold",
    "Allergen__Specific__IgE(s)__&__Total__IgE__-__Serum",
    "Glycohemoglobin",
    "Pesticides__-__Organochlorine__Metabolites__-__Serum__(Surplus)",
    "Copper,__Selenium__&__Zinc__-__Serum",
    "Cryptosporidum__&__Toxoplasma",
    "Klotho__-__Serum__(Surplus)",
    "Hepatitis__C:__Confirmed__Antibody,__RNA__(HCV-RNA),__&__Genotype",
    "Folate__-__RBC__&__Serum",
    "Metals__-__Urine__-__Special__Sample",
    "Volatile__Organic__Compounds__-__Blood__&__Related__Questionnaire__Items",
    "Human__epididymal__secretory__protein__E4__(HE4)__-__Serum__(Surplus)__(HE4)",
    "Trichomonas__-__Urine",
    "Formaldehyde",
    "Dioxins,__Furans,__&__Coplanar__PCBs",
    "Apolipoprotein__B",
    "Human__Papillomavirus__(HPV)__DNA__-__Vaginal__Swab:__Roche__Linear__Array",
    "Aromatic__Amines__-__Urine",
    "Ferritin",
]
LABORATORY_CATEGORIES, LABORATORY_CUSTOM_CATEGORIES = create_dictionaries("laboratory", LIST_LABORATORY_CATEGORIES)


LIST_QUESTIONNAIRE_CATEGORIES = [
    "Smoking__-__Cigarette_or_Tobacco__Use__-__Adult",
    "Taste__&__Smell",
    "Mental__Health__-__Panic__Disorder",
    "Creatine__Kinase",
    "Prostate__Specific__Antigen__Follow-up",
    "Prostate__Conditions",
    "Early__Childhood",
    "Volatile__Toxicant__(Subsample)",
    "Osteoporosis",
    "Hepatitis",
    "Housing__Characteristics",
    "Alcohol__Use",
    "Mental__Health__-__Depression",
    "Dermatology",
    "Consumer__Behavior",
    "Hepatitis__C__Follow__Up",
    "Diet__Behavior__&__Nutrition",
    "Cardiovascular__Health",
    "Health__Insurance",
    "Smoking__-__Adult__Recent__Tobacco__Use__&__Youth__Cigarette_or_Tobacco__Use",
    "Income",
    "Smoking__-__Secondhand__Smoke__Exposure",
    "Hospital__Utilization__&__Access__to__Care",
    "Pesticide__Use",
    "Respiratory__Health",
    "Allergy",
    "Occupation",
    "Blood__Pressure__&__Cholesterol",
    "Immunization",
    "Mental__Health__-__Depression__Screener",
    "Preventive__Aspirin__Use",
    "Medical__Conditions",
    "Social__Support",
    "Arthritis",
    "Smoking__-__Household__Smokers",
    "Reproductive__Health__-__Pregnant__Women",
    "Vision",
    "Sleep__Disorders",
    "Air__Quality",
    "Sexual__Behavior",
    "Mental__Health__-__Generalized__Anxiety__Disorder",
    "Reproductive__Health",
    "Drug__Use",
    "Consumer__Behavior__Phone__Follow-up__Module__-__Adult",
    "Alcohol__Use__-__Youth",
    "Smoking__-__Cigarette__Use",
    "Current__Health__Status",
    "Miscellaneous__Pain",
    "Physical__Functioning",
    "Balance",
    "Acculturation",
    "Food__Security",
    "Disability",
    "Physical__Activity",
    "Food__Security__-__Pregnant__Women",
    "Weight__History__-__Youth",
    "Bowel__Health",
    "Weight__History",
    "Volatile__Toxicant",
    "Cognitive__Functioning",
    "Consumer__Behavior__Phone__Follow-up__Module__-__Child",
    "Oral__Health",
    "Kidney__Conditions__-__Urology",
    "Smoking__-__Recent__Tobacco__Use",
    "Diabetes",
    "Audiometry",
    "Kidney__Conditions",
    "Tuberculosis",
]
QUESTIONNAIRE_CATEGORIES, QUESTIONNAIRE_CUSTOM_CATEGORIES = create_dictionaries(
    "questionnaire", LIST_QUESTIONNAIRE_CATEGORIES
)


CATEGORIES = {
    "examination": EXAMINATION_CATEGORIES,
    "laboratory": LABORATORY_CATEGORIES,
    "questionnaire": QUESTIONNAIRE_CATEGORIES,
}
CUSTOM_CATEGORIES = {
    "examination": EXAMINATION_CUSTOM_CATEGORIES,
    "laboratory": LABORATORY_CUSTOM_CATEGORIES,
    "questionnaire": QUESTIONNAIRE_CUSTOM_CATEGORIES,
}


ALGORITHMS = {"elastic_net": "Elastic Net", "light_gbm": "Tree based algorithm", "best": "Best"}

RANDOM_STATES = {"1": 1, "2": 2}

AXES = {"row": "Row", "column": "Column"}
AXIS_ROW, AXIS_COLUMN = list(AXES.keys())

GRAPH_SIZE = 1200
MAX_LENGTH_CATEGORY = 25
TOO_MANY_CATEGORIES = 70

DOWNLOAD_CONFIG = {"toImageButtonOptions": {"format": "svg"}}

FOLDS_RESIDUAL = {
    "train": "Metrics on the training set",
    "test": "Metrics on the testing set",
}
FOLDS_FEATURE_IMPORTANCES = {"train": "Metrics on the training set"}

SCORES_SURVIVAL = {"c_index": "C-index", "diff_c_index": "Difference C-index"}
SCORES_RESIDUAL = {
    "age": {"r2": "R??", "rmse": "RMSE"},
    "all": SCORES_SURVIVAL,
    "cvd": SCORES_SURVIVAL,
    "cancer": SCORES_SURVIVAL,
}
SCORES_FEATURE_IMPORTANCES = {
    "age": {"r2": "R??", "rmse": "RMSE"},
    "all": {"c_index": "C-index"},
    "cvd": {"c_index": "C-index"},
    "cancer": {"c_index": "C-index"},
}

AGE_COLUMN = (
    "RIDAGEEX_extended; Best age in months at date of examination for individuals under 85 years of age at screening."
)
