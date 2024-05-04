import { useEffect, useState } from "react";
import { useStates } from "../../../Hooks/useStates";
const Phone = props => {
    const { f } = useStates();
    const { image } = props;
    // console.log(image);
    const { url, name, id_image } = image;
    const unique = `phone-${name}-${id_image}`;

    return (
        <div 
            className={
                `relative 
                w-[45vw] md:w-[35vw] lg:w-[15vw] 
                h-[auto] md:h-[auto] lg:h-[auto]
                flex justify-center border border-4 border-black rounded-2xl ${unique}`
            }
            id={unique}
            >
            <img 
                src={url} alt={name} 
                className={
                    `w-[45vw] md:w-[35vw] lg:w-[15vw] 
                    h-[80vw] md:h-[70vw] lg:h-[30vw]
                    rounded-2xl`
                }
                style={{
                    boxShadow: '0 0 10px 5px rgba(0, 0, 0, 0.5)',
                    objectFit: 'cover',
                    objectPosition: 'center'
                }}
                />
            <span className="border border-black bg-black right-[18%] w-[auto] rounded-br-xl rounded-bl-xl z-10"></span>
            <span className="absolute right-[10%] top-3 bg-black border-5 border-black h-6 w-6 rounded-[50%]"></span>
            {/* <span className="absolute -right-3 top-20 bg-black border-5 border-black h-14 w-3 rounded-lg"></span>
            <span className="absolute -right-3 top-64 bg-black border-5 border-black h-20 w-3 rounded-lg"></span> */}
        </div>
    )
}

export { Phone };