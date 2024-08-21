import { useActions } from './useActions';

const useModal = (modalType:string, wrapperSelector:string | null, data:any) => {
    const {toggleModal} = useActions()

    const setModal = (currentData:any):void => {
        toggleModal({ type: modalType, data: { ...data, ...currentData } })
        const classList = document.querySelector('body')?.classList;

        modalType && !classList?.contains('modalActive') ? classList?.add('modalActive') : classList?.remove('modalActive')
    }

    const closeOnClickWrapper = (e:React.MouseEvent<any>) => {
        if (!wrapperSelector) return;

        const wrapper = document.querySelector(wrapperSelector)
        if (e.target === wrapper) {
            e.preventDefault();
            e.stopPropagation();
            toggleModal({type: '', data: {}})
        }
    }

    return {setModal, closeOnClickWrapper}
}

export default useModal;
