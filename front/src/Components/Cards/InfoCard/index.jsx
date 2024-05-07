import { useEffect, useMemo, useState } from 'react';
import styles from '../styles/info_card.module.scss';
import { useStates } from '../../../Hooks/useStates';
import { showDate } from '../../../Core/helper';
import { Phone } from '../Phone';

const InfoCard = props => {
    const { f } = useStates();
    // console.log(props);
    const { name, url, fecha_carga, model, scale, group_image, general_group, upscales, Link, categorias } = props;
    const cats = useMemo(() => categorias.filter(c => !['1x', 'original'].includes(c.nombre.toLowerCase())), [categorias]);

    const [fechaCarga, setFechaCarga] = useState(new Date());

    // w * 16 / 9
    // 160
    // 106.66666666666666
    // 53.33333333333333
    // 35.55555555555556
    // 17.77777777777778
    const cardClassName = `
        w-[90vw] h-[160.0000vw]
        sm:w-[60vw] sm:h-[106.66666666666666vw]
        md:w-[30vw] md:h-[53.33333333333333vw]
        lg:w-[20vw] lg:h-[35.55555555555556vw]
        xl:w-[10vw] xl:h-[17.77777777777778vw]
    `;
    const cardInfoClassName = `
        w-[90vw]
        sm:w-[60vw]
        md:w-[30vw]
        lg:w-[20vw]
        xl:w-[10vw]
    `;

    useEffect(() => {
        let fecha = new Date(fecha_carga);
        
        setFechaCarga(fecha);
    }, [fecha_carga]);

    return (
        <div className={`${styles.cardInfo} ${cardClassName} w-full flex flex-col items-center mx-5 mt-12`}>
            <Phone 
                image={{url, name, id_image: group_image}}
                to={`show/${group_image}`}
                Link={Link}
                block={false}
                fecha_carga={fechaCarga}
                />
            <div className={`${styles.cardInfo_info} ${cardInfoClassName} flex flex-col items-center`}>
                <h4 className={`${styles.cardInfo_title}`}>
                    <Link to={`show/${group_image}`}>
                        {name} <span className='text-sm font-normal ml-5'>{general_group}</span>
                    </Link>
                </h4>
                <Extra cats={cats} f={f}/>
            </div>
        </div>
    )
};


const Extra = props => {
    const { cats, f } = props;

    return (
        <div className={`${styles.cardInfo_categorias} flex flex-wrap`}>
            {(cats || []).map((topic, index) => {
                const Icon = topic.icon;
                return (
                    <div className={`${styles.cardInfo_topic} px-2 py-1`} key={index}>
                        <span
                            className='rounded-lg px-2 text-sm font-semibold flex items-center justify-center manita'
                            onClick={() => {
                                const cats = [topic.nombre];
                                f.u2('app', 'filtros', 'cats', cats);
                            }}
                            style={{backgroundColor: topic.bg, color: topic.color}}>
                            {topic.nombre}
                            {Icon &&
                            <Icon />}
                        </span>
                    </div>
                )
            })}
        </div>
    )
}

export { InfoCard };