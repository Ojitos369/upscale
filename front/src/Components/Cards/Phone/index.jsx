const Phone = props => {
    const image = props.image;
    console.log(image);

    const { url, model, scale } = image;

    return (
        <div className="relative flex justify-center h-[300px] w-[160px] border border-4 border-black rounded-2xl"
            style={{
                backgroundImage: `url(${url})`,
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