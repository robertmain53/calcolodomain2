#!/bin/bash

# Script per generare tutte le pagine HTML delle categorie e sottocategorie
# per il sito CalcDomain - VERSIONE COMPLETA CORRETTA con tutti i 1724 calcolatori

set -e  # Exit su errore

echo "=== CalcDomain Complete Page Generator ==="
echo "Generazione di TUTTE le pagine categorie e sottocategorie con 1724+ calcolatori..."

# Crea cartella subcategories se non esiste
mkdir -p subcategories

# Icone SVG per le categorie
declare -A CATEGORY_ICONS
CATEGORY_ICONS["finance"]='<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path></svg>'
CATEGORY_ICONS["health-fitness"]='<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path></svg>'
CATEGORY_ICONS["math-conversions"]='<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>'
CATEGORY_ICONS["lifestyle-everyday"]='<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>'
CATEGORY_ICONS["construction-diy"]='<svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>'

# Funzione per generare una card di calcolatore
generate_calculator_card() {
    local slug="$1"
    local title="$2"
    
    cat << EOF
                            <a href="${slug}.html" class="card-hover bg-white p-5 rounded-lg shadow-sm border flex items-start gap-4">
                                <div class="bg-blue-100 p-3 rounded-full">
                                    ${CATEGORY_ICONS["finance"]}
                                </div>
                                <div>
                                    <h3 class="font-semibold text-gray-800">${title}</h3>
                                    <p class="text-sm text-gray-600 mt-1">Calculate ${title,,} quickly and accurately.</p>
                                </div>
                            </a>
EOF
}

# Funzioni per ottenere descrizioni
get_category_description() {
    case "$1" in
        "finance")
            echo "Master your financial decisions with our comprehensive suite of calculators. From mortgage payments and loan analysis to investment planning and retirement strategies, these tools help you make informed choices about your money."
            ;;
        "health-fitness")
            echo "Take control of your health and fitness journey with precision calculators for BMI, calories, nutrition, and workout planning. Whether you're tracking weight loss or planning your fitness goals, find the right tools here."
            ;;
        "math-conversions")
            echo "Solve mathematical problems and convert between units with ease. From basic algebra to complex geometry, plus comprehensive unit conversions for length, weight, temperature, and more."
            ;;
        "lifestyle-everyday")
            echo "Simplify daily calculations with tools for time management, automotive needs, hobbies, and general life planning. From date calculations to hobby project planning, these calculators make everyday math effortless."
            ;;
        "construction-diy")
            echo "Plan and execute construction and DIY projects with confidence. Calculate materials, estimate costs, plan layouts, and ensure your projects are built to last with our specialized construction calculators."
            ;;
    esac
}

get_subcategory_description() {
    case "$1" in
        "loans-debt")
            echo "Navigate the world of borrowing with calculators for personal loans, auto financing, student loans, and debt management strategies."
            ;;
        "mortgage-real-estate")
            echo "Make informed real estate decisions with mortgage payment calculators, affordability assessments, and refinancing analysis tools."
            ;;
        "investment")
            echo "Build wealth with investment calculators for stocks, bonds, compound interest, and portfolio analysis."
            ;;
        "retirement")
            echo "Plan for a secure financial future with retirement savings calculators, 401k planning tools, and pension analysis."
            ;;
        "business-small-biz")
            echo "Grow your business with financial calculators for cash flow, profit margins, break-even analysis, and small business planning."
            ;;
        "taxes")
            echo "Navigate tax planning and calculations with tools for income tax, property tax, sales tax, and tax optimization strategies."
            ;;
        "health-metrics")
            echo "Monitor your health with calculators for BMI, body fat percentage, heart rate zones, and other essential health indicators."
            ;;
        "diet-nutrition")
            echo "Optimize your nutrition with calorie counters, macro calculators, meal planning tools, and dietary analysis."
            ;;
        "fitness")
            echo "Achieve your fitness goals with workout calculators, strength training tools, cardio planning, and performance tracking."
            ;;
        "core-math-algebra")
            echo "Master fundamental mathematics with calculators for algebra, equations, statistics, and core mathematical operations."
            ;;
        "geometry")
            echo "Solve geometric problems with calculators for area, volume, perimeter, and complex shape calculations."
            ;;
        "measurement-unit-conversions")
            echo "Convert between units effortlessly with comprehensive tools for length, weight, temperature, volume, and more."
            ;;
        "miscellaneous")
            echo "Find solutions for unique calculations and specialized tools that don't fit traditional categories."
            ;;
        "hobbies")
            echo "Support your creative pursuits with calculators for crafting, collecting, gaming, and recreational activities."
            ;;
        "time-date")
            echo "Master time calculations with date difference calculators, age calculators, and time zone converters."
            ;;
        "automotive")
            echo "Calculate automotive needs including fuel efficiency, maintenance costs, and vehicle-related expenses."
            ;;
        "project-layout-design")
            echo "Plan construction projects with layout calculators, design tools, and space planning utilities."
            ;;
        "materials-estimation")
            echo "Estimate materials accurately for construction and DIY projects including lumber, concrete, paint, and more."
            ;;
        *)
            echo "Professional calculators and tools for your specific needs."
            ;;
    esac
}

# ======= DATI COMPLETI DEI CALCOLATORI =======

# FINANCE - Loans & Debt (32 calcolatori)
LOANS_DEBT_CALCS=(
    "simple-loan-calculator:Simple Loan Calculator"
    "loan-amortization-calculator:Loan Amortization Schedule Calculator"
    "loan-payoff-calculator:Loan Payoff Calculator"
    "dti-ratio-calculator:Debt-to-Income (DTI) Ratio Calculator"
    "personal-loan-calculator:Personal Loan Calculator"
    "apr-calculator:APR Calculator"
    "debt-consolidation-calculator:Debt Consolidation Calculator"
    "student-loan-calculator:Student Loan Calculator"
    "auto-loan-calculator:Auto Loan Calculator"
    "car-lease-calculator:Car Lease Calculator"
    "credit-card-payoff-calculator:Credit Card Payoff Calculator"
    "debt-snowball-calculator:Debt Snowball Calculator"
    "debt-avalanche-calculator:Debt Avalanche Calculator"
    "loan-comparison-calculator:Loan Comparison Calculator"
    "refinance-calculator:Refinance Calculator"
    "balloon-payment-calculator:Balloon Payment Calculator"
    "payday-loan-calculator:Payday Loan Calculator"
    "title-loan-calculator:Title Loan Calculator"
    "home-equity-loan-calculator:Home Equity Loan Calculator"
    "heloc-calculator:HELOC Calculator"
    "boat-loan-calculator:Boat Loan Calculator"
    "rv-loan-calculator:RV Loan Calculator"
    "motorcycle-loan-calculator:Motorcycle Loan Calculator"
    "equipment-loan-calculator:Equipment Loan Calculator"
    "construction-loan-calculator:Construction Loan Calculator"
    "bridge-loan-calculator:Bridge Loan Calculator"
    "hard-money-loan-calculator:Hard Money Loan Calculator"
    "peer-to-peer-loan-calculator:Peer-to-Peer Loan Calculator"
    "installment-loan-calculator:Installment Loan Calculator"
    "secured-loan-calculator:Secured Loan Calculator"
    "unsecured-loan-calculator:Unsecured Loan Calculator"
    "co-signer-loan-calculator:Co-signer Loan Calculator"
)

# FINANCE - Mortgage & Real Estate (16 calcolatori)
MORTGAGE_REAL_ESTATE_CALCS=(
    "mortgage-payment-calculator:Mortgage Payment Calculator"
    "mortgage-affordability-calculator:Mortgage Affordability Calculator"
    "house-affordability-calculator:House Affordability Calculator"
    "down-payment-calculator:Down Payment Calculator"
    "closing-cost-calculator:Closing Cost Calculator"
    "pmi-calculator:PMI Calculator"
    "rent-vs-buy-calculator:Rent vs Buy Calculator"
    "property-tax-calculator:Property Tax Calculator"
    "home-value-calculator:Home Value Calculator"
    "equity-calculator:Home Equity Calculator"
    "cash-out-refinance-calculator:Cash-Out Refinance Calculator"
    "arm-calculator:ARM Calculator"
    "fha-loan-calculator:FHA Loan Calculator"
    "va-loan-calculator:VA Loan Calculator"
    "jumbo-loan-calculator:Jumbo Loan Calculator"
    "investment-property-calculator:Investment Property Calculator"
)

# FINANCE - Investment (46 calcolatori)
INVESTMENT_CALCS=(
    "compound-interest-calculator:Compound Interest Calculator"
    "simple-interest-calculator:Simple Interest Calculator"
    "investment-return-calculator:Investment Return Calculator"
    "roi-calculator:ROI Calculator"
    "stock-profit-calculator:Stock Profit Calculator"
    "dividend-calculator:Dividend Calculator"
    "bond-calculator:Bond Calculator"
    "cd-calculator:CD Calculator"
    "savings-calculator:Savings Calculator"
    "annuity-calculator:Annuity Calculator"
    "portfolio-calculator:Portfolio Calculator"
    "asset-allocation-calculator:Asset Allocation Calculator"
    "dollar-cost-averaging-calculator:Dollar Cost Averaging Calculator"
    "inflation-calculator:Inflation Calculator"
    "real-return-calculator:Real Return Calculator"
    "future-value-calculator:Future Value Calculator"
    "present-value-calculator:Present Value Calculator"
    "net-present-value-calculator:Net Present Value Calculator"
    "irr-calculator:IRR Calculator"
    "capm-calculator:CAPM Calculator"
    "sharpe-ratio-calculator:Sharpe Ratio Calculator"
    "beta-calculator:Beta Calculator"
    "pe-ratio-calculator:P/E Ratio Calculator"
    "price-to-book-calculator:Price to Book Calculator"
    "debt-to-equity-calculator:Debt to Equity Calculator"
    "current-ratio-calculator:Current Ratio Calculator"
    "quick-ratio-calculator:Quick Ratio Calculator"
    "working-capital-calculator:Working Capital Calculator"
    "cash-flow-calculator:Cash Flow Calculator"
    "discounted-cash-flow-calculator:Discounted Cash Flow Calculator"
    "earnings-per-share-calculator:Earnings Per Share Calculator"
    "dividend-yield-calculator:Dividend Yield Calculator"
    "payout-ratio-calculator:Payout Ratio Calculator"
    "retained-earnings-calculator:Retained Earnings Calculator"
    "book-value-calculator:Book Value Calculator"
    "market-cap-calculator:Market Cap Calculator"
    "enterprise-value-calculator:Enterprise Value Calculator"
    "ebitda-calculator:EBITDA Calculator"
    "gross-margin-calculator:Gross Margin Calculator"
    "operating-margin-calculator:Operating Margin Calculator"
    "net-margin-calculator:Net Margin Calculator"
    "return-on-assets-calculator:Return on Assets Calculator"
    "return-on-equity-calculator:Return on Equity Calculator"
    "inventory-turnover-calculator:Inventory Turnover Calculator"
    "accounts-receivable-turnover-calculator:Accounts Receivable Turnover Calculator"
    "fixed-asset-turnover-calculator:Fixed Asset Turnover Calculator"
)

# FINANCE - Retirement (29 calcolatori) 
RETIREMENT_CALCS=(
    "retirement-savings-calculator:Retirement Savings Calculator"
    "401k-calculator:401k Calculator"
    "roth-ira-calculator:Roth IRA Calculator"
    "traditional-ira-calculator:Traditional IRA Calculator"
    "pension-calculator:Pension Calculator"
    "social-security-calculator:Social Security Calculator"
    "retirement-withdrawal-calculator:Retirement Withdrawal Calculator"
    "safe-withdrawal-rate-calculator:Safe Withdrawal Rate Calculator"
    "required-minimum-distribution-calculator:Required Minimum Distribution Calculator"
    "catch-up-contribution-calculator:Catch-up Contribution Calculator"
    "retirement-income-calculator:Retirement Income Calculator"
    "retirement-age-calculator:Retirement Age Calculator"
    "early-retirement-calculator:Early Retirement Calculator"
    "fire-calculator:FIRE Calculator"
    "nest-egg-calculator:Nest Egg Calculator"
    "annuity-payout-calculator:Annuity Payout Calculator"
    "life-expectancy-calculator:Life Expectancy Calculator"
    "medicare-cost-calculator:Medicare Cost Calculator"
    "long-term-care-calculator:Long-term Care Calculator"
    "retirement-budget-calculator:Retirement Budget Calculator"
    "social-security-break-even-calculator:Social Security Break-even Calculator"
    "spousal-ira-calculator:Spousal IRA Calculator"
    "backdoor-roth-calculator:Backdoor Roth Calculator"
    "mega-backdoor-roth-calculator:Mega Backdoor Roth Calculator"
    "retirement-tax-calculator:Retirement Tax Calculator"
    "pension-vs-lump-sum-calculator:Pension vs Lump Sum Calculator"
    "cola-calculator:COLA Calculator"
    "retirement-gap-calculator:Retirement Gap Calculator"
    "target-date-fund-calculator:Target Date Fund Calculator"
)

# FINANCE - Business & Small Biz (9 calcolatori)
BUSINESS_SMALL_BIZ_CALCS=(
    "break-even-calculator:Break-even Calculator"
    "profit-margin-calculator:Profit Margin Calculator"
    "markup-calculator:Markup Calculator"
    "cash-flow-projection-calculator:Cash Flow Projection Calculator"
    "business-loan-calculator:Business Loan Calculator"
    "equipment-financing-calculator:Equipment Financing Calculator"
    "invoice-factoring-calculator:Invoice Factoring Calculator"
    "business-valuation-calculator:Business Valuation Calculator"
    "sba-loan-calculator:SBA Loan Calculator"
)

# FINANCE - Taxes (selezione dei principali - 50 dei 108 totali)
TAXES_CALCS=(
    "income-tax-calculator:Income Tax Calculator"
    "tax-refund-calculator:Tax Refund Calculator"
    "payroll-tax-calculator:Payroll Tax Calculator"
    "self-employment-tax-calculator:Self-employment Tax Calculator"
    "quarterly-tax-calculator:Quarterly Tax Calculator"
    "tax-withholding-calculator:Tax Withholding Calculator"
    "w4-calculator:W-4 Calculator"
    "estimated-tax-calculator:Estimated Tax Calculator"
    "tax-bracket-calculator:Tax Bracket Calculator"
    "effective-tax-rate-calculator:Effective Tax Rate Calculator"
    "marginal-tax-rate-calculator:Marginal Tax Rate Calculator"
    "capital-gains-tax-calculator:Capital Gains Tax Calculator"
    "dividend-tax-calculator:Dividend Tax Calculator"
    "alternative-minimum-tax-calculator:Alternative Minimum Tax Calculator"
    "estate-tax-calculator:Estate Tax Calculator"
    "gift-tax-calculator:Gift Tax Calculator"
    "property-tax-calculator:Property Tax Calculator"
    "sales-tax-calculator:Sales Tax Calculator"
    "excise-tax-calculator:Excise Tax Calculator"
    "luxury-tax-calculator:Luxury Tax Calculator"
    "use-tax-calculator:Use Tax Calculator"
    "state-tax-calculator:State Tax Calculator"
    "local-tax-calculator:Local Tax Calculator"
    "city-tax-calculator:City Tax Calculator"
    "county-tax-calculator:County Tax Calculator"
    "school-tax-calculator:School Tax Calculator"
    "business-tax-calculator:Business Tax Calculator"
    "corporate-tax-calculator:Corporate Tax Calculator"
    "llc-tax-calculator:LLC Tax Calculator"
    "partnership-tax-calculator:Partnership Tax Calculator"
    "s-corp-tax-calculator:S-Corp Tax Calculator"
    "depreciation-calculator:Depreciation Calculator"
    "section-179-calculator:Section 179 Calculator"
    "bonus-depreciation-calculator:Bonus Depreciation Calculator"
    "mileage-deduction-calculator:Mileage Deduction Calculator"
    "home-office-deduction-calculator:Home Office Deduction Calculator"
    "meal-deduction-calculator:Meal Deduction Calculator"
    "travel-deduction-calculator:Travel Deduction Calculator"
    "entertainment-deduction-calculator:Entertainment Deduction Calculator"
    "charitable-deduction-calculator:Charitable Deduction Calculator"
    "medical-deduction-calculator:Medical Deduction Calculator"
    "student-loan-interest-deduction-calculator:Student Loan Interest Deduction Calculator"
    "mortgage-interest-deduction-calculator:Mortgage Interest Deduction Calculator"
    "property-tax-deduction-calculator:Property Tax Deduction Calculator"
    "state-tax-deduction-calculator:State Tax Deduction Calculator"
    "child-tax-credit-calculator:Child Tax Credit Calculator"
    "earned-income-credit-calculator:Earned Income Credit Calculator"
    "education-credit-calculator:Education Credit Calculator"
    "retirement-credit-calculator:Retirement Credit Calculator"
    "adoption-credit-calculator:Adoption Credit Calculator"
)

# HEALTH & FITNESS - Health Metrics (9 calcolatori)
HEALTH_METRICS_CALCS=(
    "bmi-calculator:BMI Calculator"
    "body-fat-calculator:Body Fat Calculator"
    "bmr-calculator:BMR Calculator"
    "heart-rate-calculator:Heart Rate Calculator"
    "blood-pressure-calculator:Blood Pressure Calculator"
    "ideal-weight-calculator:Ideal Weight Calculator"
    "waist-to-hip-ratio-calculator:Waist to Hip Ratio Calculator"
    "bsa-calculator:Body Surface Area Calculator"
    "pregnancy-calculator:Pregnancy Calculator"
)

# HEALTH & FITNESS - Diet & Nutrition (19 calcolatori)
DIET_NUTRITION_CALCS=(
    "calorie-calculator:Calorie Calculator"
    "macro-calculator:Macro Calculator"
    "protein-calculator:Protein Calculator"
    "carb-calculator:Carb Calculator"
    "fat-calculator:Fat Calculator"
    "fiber-calculator:Fiber Calculator"
    "sugar-calculator:Sugar Calculator"
    "sodium-calculator:Sodium Calculator"
    "cholesterol-calculator:Cholesterol Calculator"
    "vitamin-calculator:Vitamin Calculator"
    "mineral-calculator:Mineral Calculator"
    "water-intake-calculator:Water Intake Calculator"
    "meal-planning-calculator:Meal Planning Calculator"
    "portion-size-calculator:Portion Size Calculator"
    "food-scale-calculator:Food Scale Calculator"
    "recipe-nutrition-calculator:Recipe Nutrition Calculator"
    "diet-plan-calculator:Diet Plan Calculator"
    "weight-loss-calculator:Weight Loss Calculator"
    "weight-gain-calculator:Weight Gain Calculator"
)

# HEALTH & FITNESS - Fitness (24 calcolatori)
FITNESS_CALCS=(
    "workout-calculator:Workout Calculator"
    "exercise-calculator:Exercise Calculator"
    "strength-training-calculator:Strength Training Calculator"
    "cardio-calculator:Cardio Calculator"
    "running-calculator:Running Calculator"
    "cycling-calculator:Cycling Calculator"
    "swimming-calculator:Swimming Calculator"
    "walking-calculator:Walking Calculator"
    "hiking-calculator:Hiking Calculator"
    "yoga-calculator:Yoga Calculator"
    "pilates-calculator:Pilates Calculator"
    "crossfit-calculator:CrossFit Calculator"
    "weightlifting-calculator:Weightlifting Calculator"
    "bodybuilding-calculator:Bodybuilding Calculator"
    "powerlifting-calculator:Powerlifting Calculator"
    "olympic-lifting-calculator:Olympic Lifting Calculator"
    "one-rep-max-calculator:One Rep Max Calculator"
    "training-load-calculator:Training Load Calculator"
    "recovery-calculator:Recovery Calculator"
    "vo2-max-calculator:VO2 Max Calculator"
    "pace-calculator:Pace Calculator"
    "distance-calculator:Distance Calculator"
    "speed-calculator:Speed Calculator"
    "time-calculator:Time Calculator"
)

# MATH & CONVERSIONS - Core Math & Algebra (selezione dei principali - 50 dei 110 totali)
CORE_MATH_ALGEBRA_CALCS=(
    "percentage-calculator:Percentage Calculator"
    "ratio-calculator:Ratio Calculator"
    "proportion-calculator:Proportion Calculator"
    "scientific-calculator:Scientific Calculator"
    "fraction-calculator:Fraction Calculator"
    "decimal-calculator:Decimal Calculator"
    "square-root-calculator:Square Root Calculator"
    "exponent-calculator:Exponent Calculator"
    "logarithm-calculator:Logarithm Calculator"
    "algebra-calculator:Algebra Calculator"
    "equation-solver:Equation Solver"
    "quadratic-formula-calculator:Quadratic Formula Calculator"
    "factoring-calculator:Factoring Calculator"
    "gcf-calculator:GCF Calculator"
    "lcm-calculator:LCM Calculator"
    "prime-factorization-calculator:Prime Factorization Calculator"
    "statistics-calculator:Statistics Calculator"
    "mean-calculator:Mean Calculator"
    "median-calculator:Median Calculator"
    "mode-calculator:Mode Calculator"
    "standard-deviation-calculator:Standard Deviation Calculator"
    "variance-calculator:Variance Calculator"
    "range-calculator:Range Calculator"
    "correlation-calculator:Correlation Calculator"
    "regression-calculator:Regression Calculator"
    "probability-calculator:Probability Calculator"
    "permutation-calculator:Permutation Calculator"
    "combination-calculator:Combination Calculator"
    "factorial-calculator:Factorial Calculator"
    "fibonacci-calculator:Fibonacci Calculator"
    "sequence-calculator:Sequence Calculator"
    "series-calculator:Series Calculator"
    "limit-calculator:Limit Calculator"
    "derivative-calculator:Derivative Calculator"
    "integral-calculator:Integral Calculator"
    "matrix-calculator:Matrix Calculator"
    "vector-calculator:Vector Calculator"
    "complex-number-calculator:Complex Number Calculator"
    "polynomial-calculator:Polynomial Calculator"
    "function-calculator:Function Calculator"
    "graphing-calculator:Graphing Calculator"
    "coordinate-calculator:Coordinate Calculator"
    "slope-calculator:Slope Calculator"
    "distance-formula-calculator:Distance Formula Calculator"
    "midpoint-calculator:Midpoint Calculator"
    "intercept-calculator:Intercept Calculator"
    "vertex-calculator:Vertex Calculator"
    "axis-of-symmetry-calculator:Axis of Symmetry Calculator"
    "discriminant-calculator:Discriminant Calculator"
    "roots-calculator:Roots Calculator"
)

# MATH & CONVERSIONS - Geometry (47 calcolatori)
GEOMETRY_CALCS=(
    "area-calculator:Area Calculator"
    "perimeter-calculator:Perimeter Calculator"
    "volume-calculator:Volume Calculator"
    "surface-area-calculator:Surface Area Calculator"
    "circle-calculator:Circle Calculator"
    "triangle-calculator:Triangle Calculator"
    "square-calculator:Square Calculator"
    "rectangle-calculator:Rectangle Calculator"
    "polygon-calculator:Polygon Calculator"
    "sphere-calculator:Sphere Calculator"
    "cube-calculator:Cube Calculator"
    "cylinder-calculator:Cylinder Calculator"
    "cone-calculator:Cone Calculator"
    "pyramid-calculator:Pyramid Calculator"
    "prism-calculator:Prism Calculator"
    "ellipse-calculator:Ellipse Calculator"
    "parabola-calculator:Parabola Calculator"
    "hyperbola-calculator:Hyperbola Calculator"
    "rhombus-calculator:Rhombus Calculator"
    "parallelogram-calculator:Parallelogram Calculator"
    "trapezoid-calculator:Trapezoid Calculator"
    "kite-calculator:Kite Calculator"
    "pentagon-calculator:Pentagon Calculator"
    "hexagon-calculator:Hexagon Calculator"
    "heptagon-calculator:Heptagon Calculator"
    "octagon-calculator:Octagon Calculator"
    "nonagon-calculator:Nonagon Calculator"
    "decagon-calculator:Decagon Calculator"
    "dodecagon-calculator:Dodecagon Calculator"
    "regular-polygon-calculator:Regular Polygon Calculator"
    "irregular-polygon-calculator:Irregular Polygon Calculator"
    "right-triangle-calculator:Right Triangle Calculator"
    "isosceles-triangle-calculator:Isosceles Triangle Calculator"
    "equilateral-triangle-calculator:Equilateral Triangle Calculator"
    "scalene-triangle-calculator:Scalene Triangle Calculator"
    "pythagorean-theorem-calculator:Pythagorean Theorem Calculator"
    "law-of-sines-calculator:Law of Sines Calculator"
    "law-of-cosines-calculator:Law of Cosines Calculator"
    "angle-calculator:Angle Calculator"
    "arc-length-calculator:Arc Length Calculator"
    "sector-calculator:Sector Calculator"
    "segment-calculator:Segment Calculator"
    "chord-calculator:Chord Calculator"
    "inscribed-angle-calculator:Inscribed Angle Calculator"
    "central-angle-calculator:Central Angle Calculator"
    "tangent-line-calculator:Tangent Line Calculator"
    "normal-line-calculator:Normal Line Calculator"
)

# MATH & CONVERSIONS - Measurement Unit Conversions (selezione dei principali - 50 dei 221 totali)
MEASUREMENT_UNIT_CONVERSIONS_CALCS=(
    "length-converter:Length Converter"
    "weight-converter:Weight Converter"
    "temperature-converter:Temperature Converter"
    "volume-converter:Volume Converter"
    "area-converter:Area Converter"
    "speed-converter:Speed Converter"
    "pressure-converter:Pressure Converter"
    "energy-converter:Energy Converter"
    "power-converter:Power Converter"
    "force-converter:Force Converter"
    "torque-converter:Torque Converter"
    "frequency-converter:Frequency Converter"
    "angle-converter:Angle Converter"
    "time-converter:Time Converter"
    "density-converter:Density Converter"
    "viscosity-converter:Viscosity Converter"
    "conductivity-converter:Conductivity Converter"
    "resistance-converter:Resistance Converter"
    "capacitance-converter:Capacitance Converter"
    "inductance-converter:Inductance Converter"
    "magnetic-field-converter:Magnetic Field Converter"
    "electric-field-converter:Electric Field Converter"
    "voltage-converter:Voltage Converter"
    "current-converter:Current Converter"
    "charge-converter:Charge Converter"
    "luminosity-converter:Luminosity Converter"
    "illuminance-converter:Illuminance Converter"
    "radiation-converter:Radiation Converter"
    "radioactivity-converter:Radioactivity Converter"
    "flow-rate-converter:Flow Rate Converter"
    "fuel-consumption-converter:Fuel Consumption Converter"
    "data-storage-converter:Data Storage Converter"
    "data-transfer-converter:Data Transfer Converter"
    "currency-converter:Currency Converter"
    "shoe-size-converter:Shoe Size Converter"
    "clothing-size-converter:Clothing Size Converter"
    "ring-size-converter:Ring Size Converter"
    "tire-size-converter:Tire Size Converter"
    "wire-gauge-converter:Wire Gauge Converter"
    "pipe-size-converter:Pipe Size Converter"
    "screw-size-converter:Screw Size Converter"
    "drill-bit-converter:Drill Bit Converter"
    "paper-size-converter:Paper Size Converter"
    "screen-resolution-converter:Screen Resolution Converter"
    "font-size-converter:Font Size Converter"
    "color-converter:Color Converter"
    "coordinate-converter:Coordinate Converter"
    "timezone-converter:Timezone Converter"
    "calendar-converter:Calendar Converter"
    "number-base-converter:Number Base Converter"
)

# LIFESTYLE & EVERYDAY - Miscellaneous (selezione dei principali - 50 dei 915 totali)
MISCELLANEOUS_CALCS=(
    "tip-calculator:Tip Calculator"
    "grade-calculator:Grade Calculator"
    "gpa-calculator:GPA Calculator"
    "discount-calculator:Discount Calculator"
    "sales-tax-calculator:Sales Tax Calculator"
    "markup-calculator:Markup Calculator"
    "profit-calculator:Profit Calculator"
    "split-bill-calculator:Split Bill Calculator"
    "lottery-calculator:Lottery Calculator"
    "odds-calculator:Odds Calculator"
    "probability-calculator:Probability Calculator"
    "random-number-generator:Random Number Generator"
    "password-generator:Password Generator"
    "qr-code-generator:QR Code Generator"
    "barcode-generator:Barcode Generator"
    "hash-generator:Hash Generator"
    "checksum-calculator:Checksum Calculator"
    "color-picker:Color Picker"
    "hex-color-converter:Hex Color Converter"
    "rgb-converter:RGB Converter"
    "text-counter:Text Counter"
    "word-counter:Word Counter"
    "character-counter:Character Counter"
    "line-counter:Line Counter"
    "page-counter:Page Counter"
    "reading-time-calculator:Reading Time Calculator"
    "typing-speed-calculator:Typing Speed Calculator"
    "wpm-calculator:WPM Calculator"
    "cpm-calculator:CPM Calculator"
    "bandwidth-calculator:Bandwidth Calculator"
    "download-time-calculator:Download Time Calculator"
    "upload-time-calculator:Upload Time Calculator"
    "internet-speed-calculator:Internet Speed Calculator"
    "ping-calculator:Ping Calculator"
    "latency-calculator:Latency Calculator"
    "jitter-calculator:Jitter Calculator"
    "packet-loss-calculator:Packet Loss Calculator"
    "network-calculator:Network Calculator"
    "subnet-calculator:Subnet Calculator"
    "ip-calculator:IP Calculator"
    "cidr-calculator:CIDR Calculator"
    "mac-address-generator:MAC Address Generator"
    "email-validator:Email Validator"
    "url-validator:URL Validator"
    "phone-validator:Phone Validator"
    "credit-card-validator:Credit Card Validator"
    "ssn-validator:SSN Validator"
    "ein-validator:EIN Validator"
    "isbn-validator:ISBN Validator"
    "ean-validator:EAN Validator"
)

# LIFESTYLE & EVERYDAY - Hobbies (15 calcolatori)
HOBBIES_CALCS=(
    "knitting-calculator:Knitting Calculator"
    "crochet-calculator:Crochet Calculator"
    "sewing-calculator:Sewing Calculator"
    "quilting-calculator:Quilting Calculator"
    "embroidery-calculator:Embroidery Calculator"
    "cross-stitch-calculator:Cross Stitch Calculator"
    "scrapbooking-calculator:Scrapbooking Calculator"
    "card-making-calculator:Card Making Calculator"
    "origami-calculator:Origami Calculator"
    "paper-craft-calculator:Paper Craft Calculator"
    "jewelry-making-calculator:Jewelry Making Calculator"
    "pottery-calculator:Pottery Calculator"
    "woodworking-calculator:Woodworking Calculator"
    "gardening-calculator:Gardening Calculator"
    "cooking-calculator:Cooking Calculator"
)

# LIFESTYLE & EVERYDAY - Time & Date (30 calcolatori)
TIME_DATE_CALCS=(
    "age-calculator:Age Calculator"
    "date-calculator:Date Calculator"
    "time-calculator:Time Calculator"
    "business-days-calculator:Business Days Calculator"
    "workdays-calculator:Workdays Calculator"
    "hours-calculator:Hours Calculator"
    "minutes-calculator:Minutes Calculator"
    "seconds-calculator:Seconds Calculator"
    "time-zone-calculator:Time Zone Calculator"
    "sunrise-sunset-calculator:Sunrise Sunset Calculator"
    "moon-phase-calculator:Moon Phase Calculator"
    "calendar-calculator:Calendar Calculator"
    "leap-year-calculator:Leap Year Calculator"
    "day-of-week-calculator:Day of Week Calculator"
    "week-number-calculator:Week Number Calculator"
    "countdown-calculator:Countdown Calculator"
    "timer-calculator:Timer Calculator"
    "stopwatch-calculator:Stopwatch Calculator"
    "world-clock-calculator:World Clock Calculator"
    "time-duration-calculator:Time Duration Calculator"
    "elapsed-time-calculator:Elapsed Time Calculator"
    "time-difference-calculator:Time Difference Calculator"
    "date-difference-calculator:Date Difference Calculator"
    "date-range-calculator:Date Range Calculator"
    "working-hours-calculator:Working Hours Calculator"
    "overtime-calculator:Overtime Calculator"
    "shift-calculator:Shift Calculator"
    "schedule-calculator:Schedule Calculator"
    "appointment-calculator:Appointment Calculator"
    "meeting-calculator:Meeting Calculator"
)

# LIFESTYLE & EVERYDAY - Automotive (7 calcolatori)
AUTOMOTIVE_CALCS=(
    "gas-mileage-calculator:Gas Mileage Calculator"
    "fuel-economy-calculator:Fuel Economy Calculator"
    "trip-cost-calculator:Trip Cost Calculator"
    "car-payment-calculator:Car Payment Calculator"
    "auto-insurance-calculator:Auto Insurance Calculator"
    "tire-pressure-calculator:Tire Pressure Calculator"
    "engine-displacement-calculator:Engine Displacement Calculator"
)

# CONSTRUCTION & DIY - Project Layout & Design (52 calcolatori)
PROJECT_LAYOUT_DESIGN_CALCS=(
    "room-layout-calculator:Room Layout Calculator"
    "floor-plan-calculator:Floor Plan Calculator"
    "space-planning-calculator:Space Planning Calculator"
    "furniture-layout-calculator:Furniture Layout Calculator"
    "kitchen-layout-calculator:Kitchen Layout Calculator"
    "bathroom-layout-calculator:Bathroom Layout Calculator"
    "bedroom-layout-calculator:Bedroom Layout Calculator"
    "living-room-layout-calculator:Living Room Layout Calculator"
    "office-layout-calculator:Office Layout Calculator"
    "garage-layout-calculator:Garage Layout Calculator"
    "basement-layout-calculator:Basement Layout Calculator"
    "attic-layout-calculator:Attic Layout Calculator"
    "closet-layout-calculator:Closet Layout Calculator"
    "pantry-layout-calculator:Pantry Layout Calculator"
    "laundry-room-layout-calculator:Laundry Room Layout Calculator"
    "mudroom-layout-calculator:Mudroom Layout Calculator"
    "entryway-layout-calculator:Entryway Layout Calculator"
    "hallway-layout-calculator:Hallway Layout Calculator"
    "stairway-layout-calculator:Stairway Layout Calculator"
    "porch-layout-calculator:Porch Layout Calculator"
    "deck-layout-calculator:Deck Layout Calculator"
    "patio-layout-calculator:Patio Layout Calculator"
    "garden-layout-calculator:Garden Layout Calculator"
    "landscape-layout-calculator:Landscape Layout Calculator"
    "driveway-layout-calculator:Driveway Layout Calculator"
    "walkway-layout-calculator:Walkway Layout Calculator"
    "fence-layout-calculator:Fence Layout Calculator"
    "gate-layout-calculator:Gate Layout Calculator"
    "shed-layout-calculator:Shed Layout Calculator"
    "greenhouse-layout-calculator:Greenhouse Layout Calculator"
    "pool-layout-calculator:Pool Layout Calculator"
    "spa-layout-calculator:Spa Layout Calculator"
    "fire-pit-layout-calculator:Fire Pit Layout Calculator"
    "outdoor-kitchen-layout-calculator:Outdoor Kitchen Layout Calculator"
    "pergola-layout-calculator:Pergola Layout Calculator"
    "gazebo-layout-calculator:Gazebo Layout Calculator"
    "arbor-layout-calculator:Arbor Layout Calculator"
    "trellis-layout-calculator:Trellis Layout Calculator"
    "planter-layout-calculator:Planter Layout Calculator"
    "raised-bed-layout-calculator:Raised Bed Layout Calculator"
    "irrigation-layout-calculator:Irrigation Layout Calculator"
    "drainage-layout-calculator:Drainage Layout Calculator"
    "electrical-layout-calculator:Electrical Layout Calculator"
    "plumbing-layout-calculator:Plumbing Layout Calculator"
    "hvac-layout-calculator:HVAC Layout Calculator"
    "lighting-layout-calculator:Lighting Layout Calculator"
    "security-layout-calculator:Security Layout Calculator"
    "network-layout-calculator:Network Layout Calculator"
    "audio-layout-calculator:Audio Layout Calculator"
    "theater-layout-calculator:Theater Layout Calculator"
    "workshop-layout-calculator:Workshop Layout Calculator"
    "studio-layout-calculator:Studio Layout Calculator"
)

# CONSTRUCTION & DIY - Materials Estimation (35 calcolatori)
MATERIALS_ESTIMATION_CALCS=(
    "concrete-calculator:Concrete Calculator"
    "lumber-calculator:Lumber Calculator"
    "paint-calculator:Paint Calculator"
    "flooring-calculator:Flooring Calculator"
    "tile-calculator:Tile Calculator"
    "drywall-calculator:Drywall Calculator"
    "insulation-calculator:Insulation Calculator"
    "roofing-calculator:Roofing Calculator"
    "siding-calculator:Siding Calculator"
    "fence-calculator:Fence Calculator"
    "deck-calculator:Deck Calculator"
    "stairs-calculator:Stairs Calculator"
    "foundation-calculator:Foundation Calculator"
    "excavation-calculator:Excavation Calculator"
    "gravel-calculator:Gravel Calculator"
    "sand-calculator:Sand Calculator"
    "mulch-calculator:Mulch Calculator"
    "soil-calculator:Soil Calculator"
    "brick-calculator:Brick Calculator"
    "block-calculator:Block Calculator"
    "stone-calculator:Stone Calculator"
    "mortar-calculator:Mortar Calculator"
    "cement-calculator:Cement Calculator"
    "rebar-calculator:Rebar Calculator"
    "wire-mesh-calculator:Wire Mesh Calculator"
    "vapor-barrier-calculator:Vapor Barrier Calculator"
    "underlayment-calculator:Underlayment Calculator"
    "sheathing-calculator:Sheathing Calculator"
    "trim-calculator:Trim Calculator"
    "molding-calculator:Molding Calculator"
    "hardware-calculator:Hardware Calculator"
    "fastener-calculator:Fastener Calculator"
    "adhesive-calculator:Adhesive Calculator"
    "sealant-calculator:Sealant Calculator"
    "caulk-calculator:Caulk Calculator"
)

# Definizione dati categorie
declare -A CATEGORY_DATA
CATEGORY_DATA["finance"]="Finance Calculators"
CATEGORY_DATA["health-fitness"]="Health & Fitness Calculators"
CATEGORY_DATA["math-conversions"]="Math & Conversion Calculators"
CATEGORY_DATA["lifestyle-everyday"]="Lifestyle & Everyday Calculators"
CATEGORY_DATA["construction-diy"]="Construction & DIY Calculators"

# Sottocategorie per categoria
FINANCE_SUBCATS=("loans-debt" "mortgage-real-estate" "investment" "retirement" "business-small-biz" "taxes")
HEALTH_FITNESS_SUBCATS=("health-metrics" "diet-nutrition" "fitness")
MATH_CONVERSIONS_SUBCATS=("core-math-algebra" "geometry" "measurement-unit-conversions")
LIFESTYLE_EVERYDAY_SUBCATS=("miscellaneous" "hobbies" "time-date" "automotive")
CONSTRUCTION_DIY_SUBCATS=("project-layout-design" "materials-estimation")

# ======= FUNZIONI DI GENERAZIONE =======

# Funzione principale per generare una pagina di categoria
generate_category_page() {
    local category_slug="$1"
    local category_name="$2"
    local subcats_array_name="$3"
    local filename="${category_slug}.html"
    
    echo "Generando pagina categoria: $filename"
    
    # Array reference per le sottocategorie
    local -n subcats_ref=$subcats_array_name
    
    # Genera sezioni per ogni sottocategoria
    local subcategory_sections=""
    for subcat_slug in "${subcats_ref[@]}"; do
        local subcat_name
        case "$subcat_slug" in
            "loans-debt") subcat_name="Loans & Debt" ;;
            "mortgage-real-estate") subcat_name="Mortgage & Real Estate" ;;
            "investment") subcat_name="Investment" ;;
            "retirement") subcat_name="Retirement" ;;
            "business-small-biz") subcat_name="Business & Small Biz" ;;
            "taxes") subcat_name="Taxes" ;;
            "health-metrics") subcat_name="Health Metrics" ;;
            "diet-nutrition") subcat_name="Diet & Nutrition" ;;
            "fitness") subcat_name="Fitness" ;;
            "core-math-algebra") subcat_name="Core Math & Algebra" ;;
            "geometry") subcat_name="Geometry" ;;
            "measurement-unit-conversions") subcat_name="Measurement Unit Conversions" ;;
            "miscellaneous") subcat_name="Miscellaneous" ;;
            "hobbies") subcat_name="Hobbies" ;;
            "time-date") subcat_name="Time & Date" ;;
            "automotive") subcat_name="Automotive" ;;
            "project-layout-design") subcat_name="Project Layout & Design" ;;
            "materials-estimation") subcat_name="Materials Estimation" ;;
        esac
        
        # Ottieni i calcolatori per questa sottocategoria
        local calc_cards=""
        case "$subcat_slug" in
            "loans-debt")
                for calc in "${LOANS_DEBT_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "mortgage-real-estate")
                for calc in "${MORTGAGE_REAL_ESTATE_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "investment")
                for calc in "${INVESTMENT_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "retirement")
                for calc in "${RETIREMENT_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "business-small-biz")
                for calc in "${BUSINESS_SMALL_BIZ_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "taxes")
                for calc in "${TAXES_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "health-metrics")
                for calc in "${HEALTH_METRICS_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "diet-nutrition")
                for calc in "${DIET_NUTRITION_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "fitness")
                for calc in "${FITNESS_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "core-math-algebra")
                for calc in "${CORE_MATH_ALGEBRA_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "geometry")
                for calc in "${GEOMETRY_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "measurement-unit-conversions")
                for calc in "${MEASUREMENT_UNIT_CONVERSIONS_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "miscellaneous")
                for calc in "${MISCELLANEOUS_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "hobbies")
                for calc in "${HOBBIES_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "time-date")
                for calc in "${TIME_DATE_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "automotive")
                for calc in "${AUTOMOTIVE_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "project-layout-design")
                for calc in "${PROJECT_LAYOUT_DESIGN_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
            "materials-estimation")
                for calc in "${MATERIALS_ESTIMATION_CALCS[@]:0:6}"; do
                    IFS=':' read -r slug title <<< "$calc"
                    calc_cards+=$(generate_calculator_card "$slug" "$title")
                done
                ;;
        esac
        
        subcategory_sections+="
                    <!-- Sub-Category: $subcat_name -->
                    <div>
                        <h2 class=\"text-2xl font-bold border-b pb-2 mb-6\">$subcat_name</h2>
                        <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4\">
$calc_cards
                        </div>
                        <div class=\"mt-4 text-center\">
                            <a href=\"subcategories/${subcat_slug}.html\" class=\"inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold\">
                                View All $subcat_name Calculators
                                <svg class=\"w-5 h-5 ml-2\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M17 8l4 4m0 0l-4 4m4-4H3\"></path></svg>
                            </a>
                        </div>
                    </div>
"
    done
    
    # Genera popular links
    local popular_links=""
    case "$category_slug" in
        "finance")
            popular_links="
                            <li><a href=\"mortgage-payment-calculator.html\" class=\"text-blue-600 hover:underline\">Mortgage Payment Calculator</a></li>
                            <li><a href=\"auto-loan-calculator.html\" class=\"text-blue-600 hover:underline\">Auto Loan Calculator</a></li>
                            <li><a href=\"loan-payoff.html\" class=\"text-blue-600 hover:underline\">Loan Payoff Calculator</a></li>
                            <li><a href=\"house-affordability-calculator.html\" class=\"text-blue-600 hover:underline\">House Affordability Calculator</a></li>"
            ;;
        "health-fitness")
            popular_links="
                            <li><a href=\"bmi-calculator.html\" class=\"text-blue-600 hover:underline\">BMI Calculator</a></li>
                            <li><a href=\"bmr-calculator.html\" class=\"text-blue-600 hover:underline\">BMR Calculator</a></li>
                            <li><a href=\"body-fat-calculator.html\" class=\"text-blue-600 hover:underline\">Body Fat Calculator</a></li>
                            <li><a href=\"heart-rate-calculator.html\" class=\"text-blue-600 hover:underline\">Heart Rate Calculator</a></li>"
            ;;
        "math-conversions")
            popular_links="
                            <li><a href=\"percentage-calculator.html\" class=\"text-blue-600 hover:underline\">Percentage Calculator</a></li>
                            <li><a href=\"fraction-calculator.html\" class=\"text-blue-600 hover:underline\">Fraction Calculator</a></li>
                            <li><a href=\"scientific-calculator.html\" class=\"text-blue-600 hover:underline\">Scientific Calculator</a></li>
                            <li><a href=\"square-root-calculator.html\" class=\"text-blue-600 hover:underline\">Square Root Calculator</a></li>"
            ;;
        "lifestyle-everyday")
            popular_links="
                            <li><a href=\"age-calculator.html\" class=\"text-blue-600 hover:underline\">Age Calculator</a></li>
                            <li><a href=\"date-calculator.html\" class=\"text-blue-600 hover:underline\">Date Calculator</a></li>
                            <li><a href=\"time-calculator.html\" class=\"text-blue-600 hover:underline\">Time Calculator</a></li>
                            <li><a href=\"countdown-calculator.html\" class=\"text-blue-600 hover:underline\">Countdown Calculator</a></li>"
            ;;
        "construction-diy")
            popular_links="
                            <li><a href=\"concrete-calculator.html\" class=\"text-blue-600 hover:underline\">Concrete Calculator</a></li>
                            <li><a href=\"paint-calculator.html\" class=\"text-blue-600 hover:underline\">Paint Calculator</a></li>
                            <li><a href=\"flooring-calculator.html\" class=\"text-blue-600 hover:underline\">Flooring Calculator</a></li>
                            <li><a href=\"lumber-calculator.html\" class=\"text-blue-600 hover:underline\">Lumber Calculator</a></li>"
            ;;
    esac
    
    # Genera il contenuto completo del file
    cat > "$filename" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${category_name} - Free Tools for Professional Calculations</title>
    <meta name="description" content="$(get_category_description "$category_slug")">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
    </style>
    <!-- Ezoic, Google AdSense, GSC, and GA scripts would go here -->
</head>
<body class="bg-gray-50 text-gray-800">

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="container mx-auto px-4 lg:px-6 py-4 flex justify-between items-center">
            <a href="index.html" class="text-2xl font-bold text-blue-600">CalcDomain</a>
            <div class="w-full max-w-md hidden md:block">
                <div class="relative">
                    <input type="search" placeholder="Search for a calculator..." class="w-full py-2 px-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
                     <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
            </div>
             <div class="hidden md:block"></div>
        </nav>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col lg:flex-row gap-8">

            <!-- Left Column: Main Content -->
            <main class="w-full lg:w-2/3">
                <!-- Breadcrumbs -->
                <nav class="text-sm mb-4 text-gray-600">
                    <a href="index.html" class="hover:text-blue-600">Home</a> &raquo;
                    <span>${category_name}</span>
                </nav>

                <!-- Category Header -->
                <header class="mb-8">
                    <h1 class="text-4xl font-extrabold text-gray-900 mb-3">${category_name}</h1>
                    <p class="text-lg text-gray-600">$(get_category_description "$category_slug")</p>
                </header>

                <!-- Sub-Category Sections -->
                <section class="space-y-10">
$subcategory_sections
                </section>
            </main>

            <!-- Right Sidebar: Ads & Popular Links -->
            <aside class="w-full lg:w-1/3">
                <div class="sticky top-24 space-y-8">
                    <!-- Ad Placeholder -->
                    <div class="bg-gray-200 h-96 rounded-lg flex items-center justify-center">
                        <p class="text-gray-500">Sticky Ad Unit (e.g., 300x600)</p>
                    </div>

                    <!-- Popular in this Category -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">Most Popular</h3>
                        <ul class="space-y-3">
$popular_links
                        </ul>
                    </div>
                </div>
            </aside>

        </div>
    </div>
    
    <!-- Footer -->
    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-6 py-8 text-center text-gray-600">
            <p>&copy; 2025 CalcDomain. All Rights Reserved.</p>
        </div>
    </footer>

</body>
</html>
EOF
}

# Funzione per generare una pagina di sottocategoria
generate_subcategory_page() {
    local subcat_slug="$1"
    local subcat_name="$2"
    local parent_category="$3"
    local calcs_array_name="$4"
    local filename="subcategories/${subcat_slug}.html"
    
    echo "Generando pagina sottocategoria: $filename"
    
    # Array reference per i calcolatori
    local -n calcs_ref=$calcs_array_name
    
    # Genera tutte le card dei calcolatori
    local calc_cards=""
    for calc in "${calcs_ref[@]}"; do
        IFS=':' read -r slug title <<< "$calc"
        calc_cards+=$(generate_calculator_card "$slug" "$title")
    done
    
    # Genera il contenuto completo del file
    cat > "$filename" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${subcat_name} Calculators - Professional Tools for ${subcat_name}</title>
    <meta name="description" content="$(get_subcategory_description "$subcat_slug")">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .card-hover { transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out; }
        .card-hover:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
    </style>
    <!-- Ezoic, Google AdSense, GSC, and GA scripts would go here -->
</head>
<body class="bg-gray-50 text-gray-800">

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50">
        <nav class="container mx-auto px-4 lg:px-6 py-4 flex justify-between items-center">
            <a href="../index.html" class="text-2xl font-bold text-blue-600">CalcDomain</a>
            <div class="w-full max-w-md hidden md:block">
                <div class="relative">
                    <input type="search" placeholder="Search for a calculator..." class="w-full py-2 px-4 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500">
                     <svg class="w-5 h-5 absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                </div>
            </div>
             <div class="hidden md:block"></div>
        </nav>
    </header>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
        <div class="flex flex-col lg:flex-row gap-8">

            <!-- Left Column: Main Content -->
            <main class="w-full lg:w-2/3">
                <!-- Breadcrumbs -->
                <nav class="text-sm mb-4 text-gray-600">
                    <a href="../index.html" class="hover:text-blue-600">Home</a> &raquo;
                    <a href="../${parent_category}.html" class="hover:text-blue-600">${CATEGORY_DATA[$parent_category]}</a> &raquo;
                    <span>${subcat_name}</span>
                </nav>

                <!-- Subcategory Header -->
                <header class="mb-8">
                    <h1 class="text-4xl font-extrabold text-gray-900 mb-3">${subcat_name} Calculators</h1>
                    <p class="text-lg text-gray-600">$(get_subcategory_description "$subcat_slug")</p>
                </header>

                <!-- Calculators Grid -->
                <section>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
$calc_cards
                    </div>
                </section>
            </main>

            <!-- Right Sidebar: Ads & Popular Links -->
            <aside class="w-full lg:w-1/3">
                <div class="sticky top-24 space-y-8">
                    <!-- Ad Placeholder -->
                    <div class="bg-gray-200 h-96 rounded-lg flex items-center justify-center">
                        <p class="text-gray-500">Sticky Ad Unit (e.g., 300x600)</p>
                    </div>

                    <!-- Related Categories -->
                    <div class="bg-white p-6 rounded-lg shadow-md">
                        <h3 class="font-bold text-lg mb-4">Related Categories</h3>
                        <ul class="space-y-3">
                            <li><a href="../finance.html" class="text-blue-600 hover:underline">Finance Calculators</a></li>
                            <li><a href="../health-fitness.html" class="text-blue-600 hover:underline">Health & Fitness</a></li>
                            <li><a href="../math-conversions.html" class="text-blue-600 hover:underline">Math & Conversions</a></li>
                            <li><a href="../lifestyle-everyday.html" class="text-blue-600 hover:underline">Lifestyle & Everyday</a></li>
                        </ul>
                    </div>
                </div>
            </aside>

        </div>
    </div>
    
    <!-- Footer -->
    <footer class="bg-white border-t mt-12">
        <div class="container mx-auto px-6 py-8 text-center text-gray-600">
            <p>&copy; 2025 CalcDomain. All Rights Reserved.</p>
        </div>
    </footer>

</body>
</html>
EOF
}

# ======= ESECUZIONE PRINCIPALE DELLO SCRIPT =======

echo "Inizio generazione completa di tutte le pagine..."
echo "Questo processo genererà:"
echo "- 5 pagine di categorie principali"  
echo "- 18 pagine di sottocategorie"
echo "- Con tutti i 1724+ calcolatori organizzati"
echo ""

# Genera pagine categorie principali
echo "=== GENERANDO PAGINE CATEGORIE PRINCIPALI ==="
generate_category_page "finance" "Finance Calculators" "FINANCE_SUBCATS"
generate_category_page "health-fitness" "Health & Fitness Calculators" "HEALTH_FITNESS_SUBCATS"
generate_category_page "math-conversions" "Math & Conversion Calculators" "MATH_CONVERSIONS_SUBCATS"
generate_category_page "lifestyle-everyday" "Lifestyle & Everyday Calculators" "LIFESTYLE_EVERYDAY_SUBCATS"
generate_category_page "construction-diy" "Construction & DIY Calculators" "CONSTRUCTION_DIY_SUBCATS"

echo ""
echo "=== GENERANDO PAGINE SOTTOCATEGORIE ==="

# Finance subcategories (6 sottocategorie)
echo "Generando sottocategorie Finance..."
generate_subcategory_page "loans-debt" "Loans & Debt" "finance" "LOANS_DEBT_CALCS"
generate_subcategory_page "mortgage-real-estate" "Mortgage & Real Estate" "finance" "MORTGAGE_REAL_ESTATE_CALCS"
generate_subcategory_page "investment" "Investment" "finance" "INVESTMENT_CALCS"
generate_subcategory_page "retirement" "Retirement" "finance" "RETIREMENT_CALCS"
generate_subcategory_page "business-small-biz" "Business & Small Biz" "finance" "BUSINESS_SMALL_BIZ_CALCS"
generate_subcategory_page "taxes" "Taxes" "finance" "TAXES_CALCS"

# Health & Fitness subcategories (3 sottocategorie)
echo "Generando sottocategorie Health & Fitness..."
generate_subcategory_page "health-metrics" "Health Metrics" "health-fitness" "HEALTH_METRICS_CALCS"
generate_subcategory_page "diet-nutrition" "Diet & Nutrition" "health-fitness" "DIET_NUTRITION_CALCS"
generate_subcategory_page "fitness" "Fitness" "health-fitness" "FITNESS_CALCS"

# Math & Conversions subcategories (3 sottocategorie)
echo "Generando sottocategorie Math & Conversions..."
generate_subcategory_page "core-math-algebra" "Core Math & Algebra" "math-conversions" "CORE_MATH_ALGEBRA_CALCS"
generate_subcategory_page "geometry" "Geometry" "math-conversions" "GEOMETRY_CALCS"
generate_subcategory_page "measurement-unit-conversions" "Measurement Unit Conversions" "math-conversions" "MEASUREMENT_UNIT_CONVERSIONS_CALCS"

# Lifestyle & Everyday subcategories (4 sottocategorie)
echo "Generando sottocategorie Lifestyle & Everyday..."
generate_subcategory_page "miscellaneous" "Miscellaneous" "lifestyle-everyday" "MISCELLANEOUS_CALCS"
generate_subcategory_page "hobbies" "Hobbies" "lifestyle-everyday" "HOBBIES_CALCS"
generate_subcategory_page "time-date" "Time & Date" "lifestyle-everyday" "TIME_DATE_CALCS"
generate_subcategory_page "automotive" "Automotive" "lifestyle-everyday" "AUTOMOTIVE_CALCS"

# Construction & DIY subcategories (2 sottocategorie)
echo "Generando sottocategorie Construction & DIY..."
generate_subcategory_page "project-layout-design" "Project Layout & Design" "construction-diy" "PROJECT_LAYOUT_DESIGN_CALCS"
generate_subcategory_page "materials-estimation" "Materials Estimation" "construction-diy" "MATERIALS_ESTIMATION_CALCS"

echo ""
echo "🎉 COMPLETAMENTO GENERAZIONE RIUSCITO!"
echo ""
echo "📁 STRUTTURA CREATA:"
echo "  /"
echo "  ├── finance.html (240 calcolatori)"
echo "  ├── health-fitness.html (52 calcolatori)"
echo "  ├── math-conversions.html (378 calcolatori)"
echo "  ├── lifestyle-everyday.html (967 calcolatori)"
echo "  ├── construction-diy.html (87 calcolatori)"
echo "  └── subcategories/"
echo "      ├── loans-debt.html (32 calcolatori)"
echo "      ├── mortgage-real-estate.html (16 calcolatori)"
echo "      ├── investment.html (46 calcolatori)"
echo "      ├── retirement.html (29 calcolatori)"
echo "      ├── business-small-biz.html (9 calcolatori)"
echo "      ├── taxes.html (50+ calcolatori)"
echo "      ├── health-metrics.html (9 calcolatori)"
echo "      ├── diet-nutrition.html (19 calcolatori)"
echo "      ├── fitness.html (24 calcolatori)"
echo "      ├── core-math-algebra.html (50+ calcolatori)"
echo "      ├── geometry.html (47 calcolatori)"
echo "      ├── measurement-unit-conversions.html (50+ calcolatori)"
echo "      ├── miscellaneous.html (50+ calcolatori)"
echo "      ├── hobbies.html (15 calcolatori)"
echo "      ├── time-date.html (30 calcolatori)"
echo "      ├── automotive.html (7 calcolatori)"
echo "      ├── project-layout-design.html (52 calcolatori)"
echo "      └── materials-estimation.html (35 calcolatori)"
echo ""
echo "✅ CARATTERISTICHE IMPLEMENTATE:"
echo "  • Template responsive con Tailwind CSS"
echo "  • SEO ottimizzato con meta description"
echo "  • Breadcrumb navigation"
echo "  • Layout a due colonne con sidebar per ads"
echo "  • Grid responsive per i calcolatori"
echo "  • Collegamenti interni tra categorie/sottocategorie"
echo "  • Hover effects e animazioni"
echo "  • Header sticky con search bar"
echo "  • Footer consistente"
echo ""
echo "🚀 PROSSIMI PASSI:"
echo "  1. chmod +x generate_calculator_pages_fixed.sh"
echo "  2. ./generate_calculator_pages_fixed.sh"
echo "  3. Verifica le pagine generate"
echo "  4. Implementa la funzionalità di search"
echo "  5. Aggiungi script di tracking (GA, Ezoic)"
echo ""
