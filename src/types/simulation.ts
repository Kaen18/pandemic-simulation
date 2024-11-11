interface SimulationConfig {
    agents: number; // obligatorio
    infected: number; // obligatorio
    distribution: DistributionConfig; // obligatorio
    ambientalParameters: AmbientalParameters; // obligatorio
    contagiousPercentage: RangePercentage; // obligatorio
    recoveryTime: RangeTime; // obligatorio
    inmunityTime?: RangeTime; // opcional, depende si siempre es requerido en la simulación
    deathPercentage: RangePercentage; // obligatorio
    simulation_time: number; // obligatorio
}

interface DistributionConfig {
    poblationalAge: AgeDistribution; // obligatorio
    healthCondition: HealthConditionDistribution; // obligatorio
    movility: MobilityDistribution; // obligatorio
    atention: AttentionDistribution; // obligatorio
    wealthyDistribution: WealthDistribution; // obligatorio
    profesionalActivity: ProfessionalActivityDistribution; // obligatorio
}

interface AgeDistribution {
    neonatal: number; // obligatorio
    kid: number; // obligatorio
    young: number; // obligatorio
    adult: number; // obligatorio
    old: number; // obligatorio
    oldest: number; // obligatorio
}

interface HealthConditionDistribution {
    athetic: number; // obligatorio
    healthy: number; // obligatorio
    sedentary: number; // obligatorio
    comorbility: number; // obligatorio
}

interface MobilityDistribution {
    restricted: number; // obligatorio
    constant: number; // obligatorio
    intermitent: number; // obligatorio
}

interface AttentionDistribution {
    low: number; // obligatorio
    medium: number; // obligatorio
    high: number; // obligatorio
}

interface WealthDistribution {
    halfMinimumSalary: number; // obligatorio
    minimumSalary: number; // obligatorio
    twoMinimumSalary: number; // obligatorio
    threeMinimumSalary: number; // obligatorio
    fiveMinimumSalary: number; // obligatorio
    tenMinimumSalary: number; // obligatorio
    moreThanTwelveMinimumSalary: number; // obligatorio
}

interface ProfessionalActivityDistribution {
    healthProfesional: number; // obligatorio
    essentialProfesional: number; // obligatorio
    normalProfesional: number; // obligatorio
    student: number; // obligatorio
    retired: number; // obligatorio
    inactive: number; // obligatorio
    domestic: number; // obligatorio
}

interface AmbientalParameters {
    quarentine: boolean; // obligatorio
    maskUse: boolean; // obligatorio
    socialDistance: boolean; // obligatorio
}

interface RangePercentage {
    minimum: number; // obligatorio
    maximum: number; // obligatorio
}

interface RangeTime {
    minimum: number; // obligatorio
    maximum: number; // obligatorio
}

export { SimulationConfig, DistributionConfig, AgeDistribution, HealthConditionDistribution, MobilityDistribution, AttentionDistribution, WealthDistribution, ProfessionalActivityDistribution, AmbientalParameters, RangePercentage, RangeTime };
