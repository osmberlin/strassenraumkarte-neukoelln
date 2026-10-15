import { Popover, PopoverButton, PopoverPanel, Transition } from '@headlessui/react'
import { Fragment } from 'react'

type Props = {
  children: React.ReactNode
}

export const NavigationMobile = ({ children }: Props) => {
  return (
    <div className="lg:hidden">
      <Popover as="div" className="inline-block text-left">
        <PopoverButton className="inline-flex w-full items-center justify-center gap-2 rounded-md border border-gray-200 bg-white py-2 pr-2 pl-4 font-medium hover:border-gray-300 hover:bg-blue-50 focus:outline-hidden focus-visible:ring-2 focus-visible:ring-white/75">
          Menu
          {/* https://fontawesome.com/v5.15/icons/bars?style=solid */}
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            className="h-8 w-8"
            viewBox="0 0 16 16"
          >
            <path
              fillRule="evenodd"
              d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5zm0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5z"
            />
          </svg>
        </PopoverButton>
        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <PopoverPanel className="absolute right-0 mt-2 w-64 origin-top-right divide-y divide-gray-100 rounded-md bg-white p-3 shadow-lg ring-1 ring-black/5 focus:outline-hidden">
            {children}
          </PopoverPanel>
        </Transition>
      </Popover>
    </div>
  )
}
