import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { BookProvider } from '../context/BookContext.jsx'
import HomePage from './HomePage.jsx'

function renderHomePage() {
  return render(
    <MemoryRouter>
      <BookProvider>
        <HomePage />
      </BookProvider>
    </MemoryRouter>,
  )
}

function addBook({ title, author, status = 'owned' }) {
  fireEvent.change(screen.getByLabelText('Judul buku'), { target: { value: title } })
  fireEvent.change(screen.getByLabelText('Penulis'), { target: { value: author } })
  fireEvent.change(screen.getByLabelText('Status buku'), { target: { value: status } })
  fireEvent.click(screen.getByRole('button', { name: 'Tambah buku' }))
}

beforeEach(() => {
  window.localStorage.clear()
})

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
})

describe('HomePage', () => {
  it('menambah buku dan menyimpannya ke localStorage', async () => {
    renderHomePage()
    addBook({ title: 'Laskar Pelangi', author: 'Andrea Hirata' })

    expect(await screen.findByRole('heading', { name: 'Laskar Pelangi' })).toBeInTheDocument()
    await waitFor(() => {
      const savedBooks = JSON.parse(window.localStorage.getItem('rak-buku-saya'))
      expect(savedBooks).toHaveLength(1)
      expect(savedBooks[0].author).toBe('Andrea Hirata')
    })
  })

  it('mencari buku dari nama penulis', () => {
    renderHomePage()
    addBook({ title: 'Laskar Pelangi', author: 'Andrea Hirata' })
    addBook({ title: 'Bumi Manusia', author: 'Pramoedya Ananta Toer' })

    fireEvent.change(screen.getByLabelText('Cari judul atau penulis'), {
      target: { value: 'Pramoedya' },
    })

    expect(screen.getByRole('heading', { name: 'Bumi Manusia' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Laskar Pelangi' })).not.toBeInTheDocument()
  })

  it('memfilter buku berdasarkan status', () => {
    renderHomePage()
    addBook({ title: 'Laskar Pelangi', author: 'Andrea Hirata', status: 'owned' })
    addBook({ title: 'Bumi Manusia', author: 'Pramoedya Ananta Toer', status: 'reading' })

    fireEvent.change(screen.getByLabelText('Filter status'), { target: { value: 'reading' } })

    expect(screen.getByRole('heading', { name: 'Bumi Manusia' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Laskar Pelangi' })).not.toBeInTheDocument()
  })

  it('mengedit data buku', async () => {
    renderHomePage()
    addBook({ title: 'Laskar Pelangi', author: 'Andrea Hirata' })

    const bookCard = screen.getByRole('listitem')
    fireEvent.click(within(bookCard).getByRole('button', { name: 'Edit' }))
    fireEvent.change(screen.getByLabelText('Judul buku'), { target: { value: 'Laskar Pelangi Baru' } })
    fireEvent.click(screen.getByRole('button', { name: 'Simpan perubahan' }))

    expect(await screen.findByRole('heading', { name: 'Laskar Pelangi Baru' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: 'Laskar Pelangi', exact: true })).not.toBeInTheDocument()
  })

  it('menghapus buku setelah mendapat konfirmasi', async () => {
    vi.spyOn(window, 'confirm').mockReturnValue(true)
    renderHomePage()
    addBook({ title: 'Laskar Pelangi', author: 'Andrea Hirata' })

    const bookCard = screen.getByRole('listitem')
    fireEvent.click(within(bookCard).getByRole('button', { name: 'Hapus' }))

    await waitFor(() => expect(screen.queryByRole('heading', { name: 'Laskar Pelangi' })).not.toBeInTheDocument())
    expect(window.confirm).toHaveBeenCalled()
  })
})
