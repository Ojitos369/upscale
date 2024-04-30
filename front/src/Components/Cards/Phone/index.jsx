import { useMemo, useState } from "react";
import { useStates } from "../../../Hooks/useStates";
const Phone = props => {
    const { f } = useStates();
    const { image } = props;
    // console.log(image);
    const { url, name, id_image } = image;
    const unique = `phone-${name}-${id_image}`;
    const [urlImage, setUrlImage] = useState(url);

    // useEffect(() => {
    //     f.app.validateUrl(url, setUrlImage);
    // }, [url]);

    return (
        <div className={`relative flex justify-center h-[300px] w-[160px] border border-4 border-black rounded-2xl ${unique}`}
            id={unique}
            style={{
                backgroundImage: `url(${urlImage})`,
                backgroundSize: 'cover',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center'
            }}
            >
            <span className="border border-black bg-black w-20 h-2 rounded-br-xl rounded-bl-xl"></span>
            <span className="absolute -right-2 top-14 border border-4 border-black h-7 rounded-md"></span>
            <span className="absolute -right-2 bottom-36 border border-4 border-black h-10 rounded-md"></span>
        </div>
    )
}

export { Phone };