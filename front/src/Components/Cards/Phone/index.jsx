import { useEffect, useState, useMemo } from "react";
import { useStates } from "../../../Hooks/useStates";
import { FingerPrint } from "../../Icons";
import styles from '../styles/phone_card.module.scss';

const Phone = props => {
    const { f } = useStates();
    const fecha = new Date();

    const { image, to, Link, block, fecha_carga, Extra, extraProps, alone } = props;

    const { url, name, id_image } = image;
    const unique = `phone-${name}-${id_image}`;

    const cardClassName = useMemo(() => !alone ? `
        ${styles.phone_container}
        w-[90vw] h-[160.0000vw]
        sm:w-[60vw] sm:h-[106.66666666666666vw]
        md:w-[30vw] md:h-[53.33333333333333vw]
        lg:w-[20vw] lg:h-[35.55555555555556vw]
        xl:w-[10vw] xl:h-[17.77777777777778vw]
    ` :
    `
        ${styles.phone_container}
        w-[90vw] h-[160.0000vw]
        sm:w-[60vw] sm:h-[106.66666666666666vw]
        md:w-[30vw] md:h-[53.33333333333333vw]
    `, [alone, styles.phone_container]);

    const cardStyle = {
        backgroundImage: `url(${url})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat'
    }

    if (!!to && !!Link) {
        return (
            <Link 
                className={cardClassName}
                style={cardStyle}
                to={to}
                id={unique}
            >
                <Content fecha={fecha_carga} block={block} Extra={Extra} extraProps={extraProps}/>
            </Link>
        )
    }

    return (
        <div 
            className={cardClassName}
            style={cardStyle}
            id={unique}
        >
            <div className={`
                ${styles.bg_defoque}
            `}>
                <Content fecha={fecha} block={block} Extra={Extra} extraProps={extraProps}/>
            </div>
        </div>
    )
}


const Content = props => {
    const { fecha, block, Extra, extraProps } = props;
    return (
        <>
            {block ?
            <>
                <p className={`${styles.hora}`}>
                    {fecha.getHours().toString().padStart(2, '0')} : {fecha.getMinutes().toString().padStart(2, '0')}
                </p>
                <p className={`${styles.fecha}`}>
                    {fecha.getDate().toString().padStart(2, '0')}/{fecha.getMonth().toString().padStart(2, '0')}/{fecha.getFullYear()}
                </p>
                <p className={`${styles.unlock}`}>
                    <span className={`${styles.icon}`}>
                        <FingerPrint />
                    </span>
                    <span className={`${styles.text}`}>
                        Desbloquear
                    </span>
                </p>
            </> : 
            <div className={`${styles.nav}`}>
                <p className={`${styles.hora}`}>
                    {fecha.getDate().toString().padStart(2, '0')}/{fecha.getMonth().toString().padStart(2, '0')}/{fecha.getFullYear()}
                </p>
            </div>
            }
            {Extra && <Extra {...extraProps}/>}
        </>
    )
}

export { Phone };