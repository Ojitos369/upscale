import { useStates } from '../../Hooks/useStates';
import { BlockPhone } from '../../Components/Cards/BlockPhone';

const Test = props => {
    const { ls, lf, s, f } = useStates();
    const image = {
        "id_image": 566,
        "name": "tw_opf_1",
        "url": "https://ojitos369.com/media/twice/ups/tw_opf_1.jpg",
        "fecha_carga": "2024-04-30T14:28:55",
        "model": "Original",
        "scale": "1x",
        "group_image": "tw_opf_1",
        "general_group": "tw_opf",
        "categorias": [
            {
                "nombre": "1X",
                "bg": "#513dbd",
                "color": "#000000"
            },
            {
                "nombre": "NAYEON",
                "bg": "#49c0ec",
                "color": "#000000"
            },
            {
                "nombre": "ORIGINAL",
                "bg": "#836ddb",
                "color": "#000000"
            },
            {
                "nombre": "TWICE",
                "bg": "#fc5d9d",
                "color": "#000000"
            }
        ]
    }
    return (
        <>
            <BlockPhone image={image} />
        </>
    )
}

export { Test };
