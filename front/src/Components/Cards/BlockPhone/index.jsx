import { useEffect, useState } from "react";
import { useStates } from "../../../Hooks/useStates";
import { FingerPrint } from "../../Icons";
import styles from '../styles/block_phone_card.module.scss';
const BlockPhone = props => {
    const { f } = useStates();
    const [fecha, setFecha] = useState(new Date());

    const { image } = props;
    // console.log(image);
    const { url, name, id_image } = image;
    const unique = `phone-${name}-${id_image}`;

    // <span>{fecha.getHours().toString().padStart(2, '0')}</span>
    // <span>{fecha.getMinutes().toString().padStart(2, '0')}</span>

    return (
        <div 
            className={`
                ${styles.block_phone_container}
                w-[90vw] h-[160.0000vw]
                sm:w-[60vw] sm:h-[106.66666666666666vw]
                md:w-[30vw] md:h-[53.33333333333333vw]
                lg:w-[20vw] lg:h-[35.55555555555556vw]
                xl:w-[10vw] xl:h-[17.77777777777778vw]
            `}
            style={{
                backgroundImage: `url(${url})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat'
            }}
        >
            <div className={`
                    ${styles.bg_defoque}
                `}>
            
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

            </div>
        </div>
    )
}

export { BlockPhone };