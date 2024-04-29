import { useMemo } from 'react';
import styles from '../styles/info_card.module.scss';
import { useStates } from '../../../Hooks/useStates';
import { showDate } from '../../../Core/helper';


const InfoCard = props => {
    const { f } = useStates();
    // console.log(props);
    const { name, url, fecha_carga, model, scale, group_image, general_group, upscales, Link, categorias } = props;
    const cats = useMemo(() => categorias.filter(c => !['1x', '2x'].includes(c.nombre.toLowerCase())), [categorias]);

    const stylesBanner = useMemo(() => {
        if (url) {
            return {
                backgroundImage: `url(${url})`,
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center'
            }
        } else {
            return {
                backgroundColor: 'gray'
            }
        }
    }, [props]);

    return (
        <div className={`${styles.cardInfo_container} mt-10`}>
            <div className={`${styles.cardInfo_head}`}
                style={stylesBanner}>
                <span className={`${styles.cardInfo_head_span}`}>
                    {showDate(fecha_carga)}
                </span>
            </div>
            <div className={`${styles.cardInfo_body}`}>
                <h4 className={`${styles.cardInfo_title}`}>
                    <Link to={`show/${group_image}`}>
                        {name} <span className='text-sm font-normal ml-5'>{general_group}</span>
                    </Link>
                </h4>
                {/* <p className={`${styles.cardInfo_description}`}>
                    {descripcion}
                </p> */}

                <div className={`${styles.cardInfo_categorias} flex flex-wrap w-full`}>
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
            </div>
        </div>
    )
};

export { InfoCard };